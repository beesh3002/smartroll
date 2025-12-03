import 'package:http/http.dart' as http;
import 'package:my_app/data/base_url.dart';
import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';

Future<void> registerDevice(int studentId) async {
  final response = await http.post(
    Uri.parse('$baseURL/auth/register_device'),
    headers: {'Content-Type': 'application/json'},
    body: jsonEncode({'student_id': studentId}),
  );

  print(response);

  if (response.statusCode == 200) {
    final data = jsonDecode(response.body);
    final token = data['device_token'];
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('device_token', token);
    print('Device token stored locally: $token');
  } else {
    print('Failed to register device: ${response.body}');
  }
}
