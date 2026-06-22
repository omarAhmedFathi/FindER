import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'emergency_provider.dart';
import '../../models/emergency.dart';

class EmergencyListScreen extends ConsumerStatefulWidget {
  const EmergencyListScreen({super.key});

  @override
  ConsumerState<EmergencyListScreen> createState() => _EmergencyListScreenState();
}

class _EmergencyListScreenState extends ConsumerState<EmergencyListScreen> {
  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      ref.read(emergencyProvider.notifier).loadEmergencies();
    });
  }

  Color _severityColor(int s) {
    if (s >= 5) return Colors.red.shade700;
    if (s >= 4) return Colors.orange.shade700;
    if (s >= 3) return Colors.amber.shade700;
    return Colors.green.shade700;
  }

  Color _statusColor(String s) {
    switch (s) {
      case 'ACTIVE': return Colors.red;
      case 'ROUTED': return Colors.orange;
      case 'RESOLVED': return Colors.green;
      default: return Colors.grey;
    }
  }

  @override
  Widget build(BuildContext context) {
    final state = ref.watch(emergencyProvider);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Emergencies'),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: () => ref.read(emergencyProvider.notifier).loadEmergencies(),
          ),
        ],
      ),
      body: state.isLoading
          ? const Center(child: CircularProgressIndicator())
          : state.error != null
              ? Center(
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      const Icon(Icons.error_outline, size: 48, color: Colors.red),
                      const SizedBox(height: 12),
                      Text(state.error!),
                      const SizedBox(height: 12),
                      ElevatedButton(
                        onPressed: () => ref.read(emergencyProvider.notifier).loadEmergencies(),
                        child: const Text('Retry'),
                      ),
                    ],
                  ),
                )
              : state.emergencies.isEmpty
                  ? const Center(
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Icon(Icons.check_circle_outline, size: 64, color: Colors.green),
                          SizedBox(height: 12),
                          Text('No emergencies reported', style: TextStyle(fontSize: 16)),
                        ],
                      ),
                    )
                  : RefreshIndicator(
                      onRefresh: () => ref.read(emergencyProvider.notifier).loadEmergencies(),
                      child: ListView.builder(
                        padding: const EdgeInsets.all(12),
                        itemCount: state.emergencies.length,
                        itemBuilder: (ctx, i) => _EmergencyCard(
                          emergency: state.emergencies[i],
                          severityColor: _severityColor(state.emergencies[i].severity),
                          statusColor: _statusColor(state.emergencies[i].status),
                        ),
                      ),
                    ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () => context.push('/emergencies/report'),
        backgroundColor: const Color(0xFFD32F2F),
        icon: const Icon(Icons.add_alert, color: Colors.white),
        label: const Text('Report', style: TextStyle(color: Colors.white)),
      ),
    );
  }
}

class _EmergencyCard extends StatelessWidget {
  final Emergency emergency;
  final Color severityColor;
  final Color statusColor;

  const _EmergencyCard({
    required this.emergency,
    required this.severityColor,
    required this.statusColor,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.only(bottom: 10),
      elevation: 2,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12),
        side: BorderSide(color: severityColor.withOpacity(0.3)),
      ),
      child: Padding(
        padding: const EdgeInsets.all(14),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                  decoration: BoxDecoration(
                    color: severityColor,
                    borderRadius: BorderRadius.circular(6),
                  ),
                  child: Text(
                    emergency.severityLabel,
                    style: const TextStyle(color: Colors.white, fontSize: 11, fontWeight: FontWeight.bold),
                  ),
                ),
                const SizedBox(width: 8),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                  decoration: BoxDecoration(
                    color: statusColor.withOpacity(0.1),
                    borderRadius: BorderRadius.circular(6),
                    border: Border.all(color: statusColor),
                  ),
                  child: Text(
                    emergency.status,
                    style: TextStyle(color: statusColor, fontSize: 11, fontWeight: FontWeight.bold),
                  ),
                ),
                const Spacer(),
                Icon(Icons.location_on, size: 14, color: Colors.grey.shade500),
                Text(
                  '${emergency.locationLat.toStringAsFixed(3)}, ${emergency.locationLon.toStringAsFixed(3)}',
                  style: TextStyle(fontSize: 11, color: Colors.grey.shade600),
                ),
              ],
            ),
            if (emergency.description != null) ...[
              const SizedBox(height: 8),
              Text(
                emergency.description!,
                style: const TextStyle(fontSize: 14),
                maxLines: 2,
                overflow: TextOverflow.ellipsis,
              ),
            ],
            const SizedBox(height: 6),
            Text(
              emergency.createdAt.substring(0, 19).replaceAll('T', ' '),
              style: TextStyle(fontSize: 11, color: Colors.grey.shade500),
            ),
          ],
        ),
      ),
    );
  }
}
