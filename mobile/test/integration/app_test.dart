import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:finder/main.dart' as app;

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  testWidgets('end-to-end authentication and SOS trigger flow', (WidgetTester tester) async {
    app.main();
    await tester.pumpAndSettle();

    // 1. Assert Login Page
    expect(find.text('FindER'), findsOneWidget);

    // 2. Enter credentials
    await tester.enterText(find.bySemanticsLabel('Email'), 'medic@finder.app');
    await tester.enterText(find.bySemanticsLabel('Password'), 'securepass123');
    await tester.tap(find.text('Secure Login'));
    
    // Wait for API response and animations
    await tester.pumpAndSettle(const Duration(seconds: 3));

    // 3. Assert Dashboard reached
    expect(find.text('Situational Awareness'), findsOneWidget);
    
    // 4. Navigate to SOS
    await tester.tap(find.byIcon(Icons.warning));
    await tester.pumpAndSettle();
    
    // 5. Trigger SOS
    expect(find.text('Emergency SOS'), findsOneWidget);
  });
}
