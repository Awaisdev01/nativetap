// ✅ Written WITH nativetap — every row cited in comments.
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

class CheckoutPage extends StatefulWidget {
  const CheckoutPage({super.key});
  @override
  State<CheckoutPage> createState() => _CheckoutPageState();
}

class _CheckoutPageState extends State<CheckoutPage> {
  final _controller = TextEditingController();
  String? _error; // forms: validate on submit, not per keystroke

  void _submit() {
    setState(() => _error =
        _controller.text.length < 12 ? 'Check the card number' : null);
    if (_error == null) {
      HapticFeedback.lightImpact(); // gestures: haptic marks state change
      // motion: success confirmation 300-500ms check-bounce
    }
  }

  @override
  Widget build(BuildContext context) {
    // safe-areas: keyboard pushes content, never covers the focused field
    return Scaffold(
      resizeToAvoidBottomInset: true,
      appBar: AppBar(title: const Text('Checkout')),
      body: Padding(
        padding: const EdgeInsets.all(16), // components: 16dp edge padding
        child: Column(
          children: [
            // a11y: flexible height survives 200% font scale (thumb rule #6)
            TextField(
              controller: _controller,
              keyboardType: TextInputType.number, // forms: match input semantics
              textInputAction: TextInputAction.done, // forms: action = submit
              autofillHints: const [AutofillHints.creditCardNumber],
              decoration: InputDecoration(
                labelText: 'Card number', // thumb rule: labels above/visible
                errorText: _error, // forms: inline error under the field
              ),
            ),
            const Spacer(),
            // thumb rule #1/#2: 48dp target, bottom of screen = thumb zone,
            // full-width = no adjacent-target ambiguity (8px rule)
            SizedBox(
              width: double.infinity,
              height: 48,
              child: FilledButton(onPressed: _submit, child: const Text('Pay now')),
            ),
          ],
        ),
      ),
    );
  }
}
