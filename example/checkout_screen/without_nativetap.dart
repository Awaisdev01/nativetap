// ❌ Written WITHOUT nativetap — web instincts on a phone screen.
import 'package:flutter/material.dart';

class CheckoutPage extends StatelessWidget {
  const CheckoutPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Checkout')),
      body: Column(
        children: [
          // Fixed height clips at 200% font scale (thumb rule #6)
          Container(
            height: 48,
            padding: const EdgeInsets.all(8),
            child: const TextField(decoration: InputDecoration(labelText: 'Card number')),
          ),
          // Top-right submit: unreachable one-handed (thumb rule #2)
          // 32pt target: too small (thumb rule #1), targets < 8px apart
          Row(
            mainAxisAlignment: MainAxisAlignment.end,
            children: [
              TextButton(onPressed: () {}, child: const Text('Back')),
              const SizedBox(width: 4),
              TextButton(onPressed: () {}, child: const Text('Submit')),
            ],
          ),
        ],
      ),
    );
  }
}
