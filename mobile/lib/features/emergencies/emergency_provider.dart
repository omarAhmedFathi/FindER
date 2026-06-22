import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../core/api_client.dart';
import '../../models/emergency.dart';

class EmergencyState {
  final List<Emergency> emergencies;
  final bool isLoading;
  final String? error;

  const EmergencyState({
    this.emergencies = const [],
    this.isLoading = false,
    this.error,
  });

  EmergencyState copyWith({List<Emergency>? emergencies, bool? isLoading, String? error}) =>
      EmergencyState(
        emergencies: emergencies ?? this.emergencies,
        isLoading: isLoading ?? this.isLoading,
        error: error,
      );
}

class EmergencyNotifier extends StateNotifier<EmergencyState> {
  final ApiClient _api = ApiClient();

  EmergencyNotifier() : super(const EmergencyState());

  Future<void> loadEmergencies() async {
    state = state.copyWith(isLoading: true, error: null);
    try {
      final data = await _api.getEmergencies();
      final emergencies = data.map((e) => Emergency.fromJson(e as Map<String, dynamic>)).toList();
      state = state.copyWith(emergencies: emergencies, isLoading: false);
    } catch (e) {
      state = state.copyWith(isLoading: false, error: 'Failed to load emergencies');
    }
  }

  Future<bool> reportEmergency({
    required double lat,
    required double lon,
    required String description,
    required int severity,
    bool isAnonymous = false,
  }) async {
    try {
      final data = await _api.createEmergency(
        lat: lat,
        lon: lon,
        description: description,
        severity: severity,
        isAnonymous: isAnonymous,
      );
      final emergency = Emergency.fromJson(data);
      state = state.copyWith(emergencies: [emergency, ...state.emergencies]);
      return true;
    } catch (e) {
      return false;
    }
  }

  Future<bool> triggerSOS({required double lat, required double lon}) async {
    try {
      final data = await _api.triggerSOS(lat: lat, lon: lon);
      final emergency = Emergency.fromJson(data);
      state = state.copyWith(emergencies: [emergency, ...state.emergencies]);
      return true;
    } catch (e) {
      return false;
    }
  }
}

final emergencyProvider = StateNotifierProvider<EmergencyNotifier, EmergencyState>(
  (ref) => EmergencyNotifier(),
);
