class Hospital {
  final String id;
  final String name;
  final double locationLat;
  final double locationLon;
  final int totalBeds;
  final int availableBeds;
  final int traumaLevel;

  const Hospital({
    required this.id,
    required this.name,
    required this.locationLat,
    required this.locationLon,
    required this.totalBeds,
    required this.availableBeds,
    required this.traumaLevel,
  });

  factory Hospital.fromJson(Map<String, dynamic> json) => Hospital(
        id: json['id'] as String,
        name: json['name'] as String,
        locationLat: (json['location_lat'] as num).toDouble(),
        locationLon: (json['location_lon'] as num).toDouble(),
        totalBeds: json['total_beds'] as int,
        availableBeds: json['available_beds'] as int,
        traumaLevel: json['trauma_level'] as int,
      );

  double get occupancyRate => totalBeds > 0 ? (totalBeds - availableBeds) / totalBeds : 0;
  bool get hasCapacity => availableBeds > 0;
}
