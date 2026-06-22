import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:hive_flutter/hive_flutter.dart';
import '../../core/api_client.dart';
import '../../models/user.dart';

class AuthState {
  final User? user;
  final bool isLoading;
  final String? error;
  final bool isAuthenticated;

  const AuthState({
    this.user,
    this.isLoading = false,
    this.error,
    this.isAuthenticated = false,
  });

  AuthState copyWith({
    User? user,
    bool? isLoading,
    String? error,
    bool? isAuthenticated,
  }) => AuthState(
        user: user ?? this.user,
        isLoading: isLoading ?? this.isLoading,
        error: error,
        isAuthenticated: isAuthenticated ?? this.isAuthenticated,
      );
}

class AuthNotifier extends StateNotifier<AuthState> {
  final ApiClient _api = ApiClient();

  AuthNotifier() : super(const AuthState()) {
    _checkToken();
  }

  void _checkToken() {
    final box = Hive.box('auth');
    final token = box.get('access_token');
    if (token != null) {
      state = state.copyWith(isAuthenticated: true);
      _loadUser();
    }
  }

  Future<void> _loadUser() async {
    try {
      final data = await _api.getMe();
      state = state.copyWith(user: User.fromJson(data), isAuthenticated: true);
    } catch (_) {
      logout();
    }
  }

  Future<bool> login(String email, String password) async {
    state = state.copyWith(isLoading: true, error: null);
    try {
      final data = await _api.login(email: email, password: password);
      final box = Hive.box('auth');
      await box.put('access_token', data['access_token']);
      await box.put('refresh_token', data['refresh_token']);
      await _loadUser();
      state = state.copyWith(isLoading: false, isAuthenticated: true);
      return true;
    } catch (e) {
      state = state.copyWith(isLoading: false, error: _parseError(e));
      return false;
    }
  }

  Future<bool> register({
    required String email,
    required String password,
    required String fullName,
    required String role,
  }) async {
    state = state.copyWith(isLoading: true, error: null);
    try {
      await _api.register(email: email, password: password, fullName: fullName, role: role);
      return await login(email, password);
    } catch (e) {
      state = state.copyWith(isLoading: false, error: _parseError(e));
      return false;
    }
  }

  void logout() {
    final box = Hive.box('auth');
    box.delete('access_token');
    box.delete('refresh_token');
    state = const AuthState();
  }

  String _parseError(Object e) {
    if (e.toString().contains('400')) return 'Email already registered';
    if (e.toString().contains('401')) return 'Invalid email or password';
    if (e.toString().contains('Connection')) return 'Cannot connect to server';
    return 'An error occurred. Please try again.';
  }
}

final authProvider = StateNotifierProvider<AuthNotifier, AuthState>((ref) => AuthNotifier());
