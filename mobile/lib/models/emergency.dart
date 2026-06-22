class Emergency {
  final String id;
  final String? reporterId;
  final String status;
  final double locationLat;
  final double locationLon;
  final String? description;
  final int severity;
  final bool detectedViaNlp;
  final String createdAt;

  const Emergency({
    required this.id,
    this.reporterId,
    required this.status,
    required this.locationLat,
    required this.locationLon,
    this.description,
    required this.severity,
    required this.detectedViaNlp,
    required this.createdAt,
  });

  factory Emergency.fromJson(Map<String, dynamic> json) => Emergency(
        id: json['id'] as String,
        reporterId: json['reporter_id'] as String?,
        status: json['status'] as String,
        locationLat: (json['location_lat'] as num).toDouble(),
        locationLon: (json['location_lon'] as num).toDouble(),
        description: json['description'] as String?,
        severity: json['severity'] as int? ?? 3,
        detectedViaNlp: json['detected_via_nlp'] as bool? ?? false,
        createdAt: json['created_at'] as String,
      );

  String get severityLabel {
    switch (severity) {
      case 5: return 'CRITICAL';
      case 4: return 'HIGH';
      case 3: return 'MEDIUM';
      case 2: return 'LOW';
      default: return 'MINIMAL';
    }
  }

  String get statusLabel => status;
}
