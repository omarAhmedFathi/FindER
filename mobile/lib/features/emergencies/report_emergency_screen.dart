import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'emergency_provider.dart';

class ReportEmergencyScreen extends ConsumerStatefulWidget {
  const ReportEmergencyScreen({super.key});

  @override
  ConsumerState<ReportEmergencyScreen> createState() => _ReportEmergencyScreenState();
}

class _ReportEmergencyScreenState extends ConsumerState<ReportEmergencyScreen> {
  final _formKey = GlobalKey<FormState>();
  final _descCtrl = TextEditingController();
  final _latCtrl = TextEditingController(text: '37.7749');
  final _lonCtrl = TextEditingController(text: '-122.4194');
  int _severity = 3;
  bool _isAnonymous = false;
  bool _isSubmitting = false;

  @override
  void dispose() {
    _descCtrl.dispose();
    _latCtrl.dispose();
    _lonCtrl.dispose();
    super.dispose();
  }

  Future<void> _submit() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() => _isSubmitting = true);
    final ok = await ref.read(emergencyProvider.notifier).reportEmergency(
          lat: double.parse(_latCtrl.text),
          lon: double.parse(_lonCtrl.text),
          description: _descCtrl.text.trim(),
          severity: _severity,
          isAnonymous: _isAnonymous,
        );
    setState(() => _isSubmitting = false);
    if (mounted) {
      if (ok) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Emergency reported!'), backgroundColor: Colors.green),
        );
        context.pop();
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Failed to report. Check connection.'), backgroundColor: Colors.red),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Report Emergency')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Form(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: Colors.red.shade50,
                  borderRadius: BorderRadius.circular(12),
                  border: Border.all(color: Colors.red.shade200),
                ),
                child: Row(
                  children: [
                    Icon(Icons.warning_amber, color: Colors.red.shade700, size: 28),
                    const SizedBox(width: 12),
                    Expanded(
                      child: Text(
                        'For life-threatening emergencies, call 911 immediately.',
                        style: TextStyle(color: Colors.red.shade700, fontWeight: FontWeight.w500),
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 24),
              const Text('Location', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
              const SizedBox(height: 10),
              Row(
                children: [
                  Expanded(
                    child: TextFormField(
                      controller: _latCtrl,
                      keyboardType: const TextInputType.numberWithOptions(decimal: true),
                      decoration: const InputDecoration(
                        labelText: 'Latitude',
                        border: OutlineInputBorder(),
                        prefixIcon: Icon(Icons.location_on),
                      ),
                      validator: (v) {
                        final d = double.tryParse(v ?? '');
                        return d == null ? 'Invalid' : null;
                      },
                    ),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: TextFormField(
                      controller: _lonCtrl,
                      keyboardType: const TextInputType.numberWithOptions(decimal: true),
                      decoration: const InputDecoration(
                        labelText: 'Longitude',
                        border: OutlineInputBorder(),
                      ),
                      validator: (v) {
                        final d = double.tryParse(v ?? '');
                        return d == null ? 'Invalid' : null;
                      },
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 20),
              const Text('Description', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
              const SizedBox(height: 10),
              TextFormField(
                controller: _descCtrl,
                maxLines: 4,
                decoration: const InputDecoration(
                  hintText: 'Describe the emergency situation...',
                  border: OutlineInputBorder(),
                ),
                validator: (v) => (v == null || v.trim().length < 5) ? 'Please describe the emergency' : null,
              ),
              const SizedBox(height: 20),
              Row(
                children: [
                  const Text('Severity:', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
                  const SizedBox(width: 12),
                  Expanded(
                    child: Slider(
                      value: _severity.toDouble(),
                      min: 1,
                      max: 5,
                      divisions: 4,
                      activeColor: _severity >= 4
                          ? Colors.red
                          : _severity >= 3
                              ? Colors.orange
                              : Colors.green,
                      label: _severityLabel(_severity),
                      onChanged: (v) => setState(() => _severity = v.round()),
                    ),
                  ),
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                    decoration: BoxDecoration(
                      color: _severity >= 4 ? Colors.red : _severity >= 3 ? Colors.orange : Colors.green,
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: Text(
                      _severityLabel(_severity),
                      style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold),
                    ),
                  ),
                ],
              ),
              SwitchListTile(
                title: const Text('Report anonymously'),
                subtitle: const Text('Your identity will not be attached'),
                value: _isAnonymous,
                onChanged: (v) => setState(() => _isAnonymous = v),
                contentPadding: EdgeInsets.zero,
              ),
              const SizedBox(height: 24),
              ElevatedButton.icon(
                onPressed: _isSubmitting ? null : _submit,
                icon: _isSubmitting
                    ? const SizedBox(width: 18, height: 18, child: CircularProgressIndicator(color: Colors.white, strokeWidth: 2))
                    : const Icon(Icons.send),
                label: Text(_isSubmitting ? 'Submitting...' : 'Submit Report'),
              ),
            ],
          ),
        ),
      ),
    );
  }

  String _severityLabel(int s) {
    const labels = {1: 'MINIMAL', 2: 'LOW', 3: 'MEDIUM', 4: 'HIGH', 5: 'CRITICAL'};
    return labels[s] ?? 'MEDIUM';
  }
}
