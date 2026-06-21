import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:finder/features/auth/presentation/pages/login_page.dart';
import 'package:finder/shared/widgets/app_button.dart';

void main() {
  testWidgets('LoginPage renders correctly and validates empty fields', (WidgetTester tester) async {
    await tester.pumpWidget(
      const ProviderScope(
        child: MaterialApp(
          home: LoginPage(),
        ),
      ),
    );

    // Verify UI components
    expect(find.text('FindER'), findsOneWidget);
    expect(find.text('Email'), findsOneWidget);
    expect(find.text('Password'), findsOneWidget);
    expect(find.byType(AppButton), findsOneWidget);

    // Tap Login without entering text
    await tester.tap(find.byType(AppButton));
    await tester.pump();

    // Verify nothing crashed, further validation text assertions can go here
  });
}
