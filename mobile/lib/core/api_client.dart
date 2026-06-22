import 'package:dio/dio.dart';
import 'package:hive_flutter/hive_flutter.dart';

const String _baseUrl = 'https://find-er--seifkh021.replit.app/api/v1';

class ApiClient {
  static final ApiClient _instance = ApiClient._internal();
  factory ApiClient() => _instance;

  late final Dio _dio;

  ApiClient._internal() {
    _dio = Dio(BaseOptions(
      baseUrl: _baseUrl,
      connectTimeout: const Duration(seconds: 10),
      receiveTimeout: const Duration(seconds: 15),
      headers: {'Content-Type': 'application/json'},
    ));

    _dio.interceptors.add(InterceptorsWrapper(
      onRequest: (options, handler) {
        final box = Hive.box('auth');
        final token = box.get('access_token');
        if (token != null) {
          options.headers['Authorization'] = 'Bearer $token';
        }
        handler.next(options);
      },
      onError: (error, handler) {
        handler.next(error);
      },
    ));
  }

  Dio get dio => _dio;

  Future<Map<String, dynamic>> register({
    required String email,
    required String password,
    required String fullName,
    required String role,
  }) async {
    final response = await _dio.post('/auth/register', data: {
      'email': email,
      'password': password,
      'full_name': fullName,
      'role': role,
    });
    return response.data as Map<String, dynamic>;
  }

  Future<Map<String, dynamic>> login({
    required String email,
    required String password,
  }) async {
    final response = await _dio.post('/auth/login', data: {
      'email': email,
      'password': password,
    });
    return response.data as Map<String, dynamic>;
  }

  Future<Map<String, dynamic>> getMe() async {
    final response = await _dio.get('/auth/me');
    return response.data as Map<String, dynamic>;
  }

  Future<List<dynamic>> getEmergencies({String? statusFilter}) async {
    final params = statusFilter != null ? {'status_filter': statusFilter} : null;
    final response = await _dio.get('/emergencies/', queryParameters: params);
    return response.data as List<dynamic>;
  }

  Future<List<dynamic>> getActiveEmergencies() async {
    final response = await _dio.get('/emergencies/active');
    return response.data as List<dynamic>;
  }

  Future<Map<String, dynamic>> createEmergency({
    required double lat,
    required double lon,
    required String description,
    required int severity,
    bool isAnonymous = false,
  }) async {
    final response = await _dio.post('/emergencies/', data: {
      'location_lat': lat,
      'location_lon': lon,
      'description': description,
      'severity': severity,
      'is_anonymous': isAnonymous,
    });
    return response.data as Map<String, dynamic>;
  }

  Future<Map<String, dynamic>> triggerSOS({
    required double lat,
    required double lon,
    String? description,
  }) async {
    final response = await _dio.post('/emergencies/sos', data: {
      'location_lat': lat,
      'location_lon': lon,
      'description': description ?? 'SOS Alert',
      'severity': 5,
      'is_anonymous': false,
    });
    return response.data as Map<String, dynamic>;
  }

  Future<List<dynamic>> getHospitals() async {
    final response = await _dio.get('/hospitals/');
    return response.data as List<dynamic>;
  }

  Future<List<dynamic>> getNearestHospitals(double lat, double lon) async {
    final response = await _dio.get('/hospitals/nearest', queryParameters: {
      'lat': lat,
      'lon': lon,
    });
    return response.data as List<dynamic>;
  }

  Future<List<dynamic>> getResources({String? type}) async {
    final params = type != null ? {'resource_type': type} : null;
    final response = await _dio.get('/resources/', queryParameters: params);
    return response.data as List<dynamic>;
  }

  Future<Map<String, dynamic>> healthCheck() async {
    final response = await _dio.get('/health/');
    return response.data as Map<String, dynamic>;
  }
}
