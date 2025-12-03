import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

import 'data/base_url.dart';

class HistoryPage extends StatefulWidget {
  final int studentId;
  final int sessionId;

  const HistoryPage({
    super.key,
    required this.studentId,
    required this.sessionId,
  });

  @override
  State<HistoryPage> createState() => _HistoryPageState();
}

class _HistoryPageState extends State<HistoryPage> {
  List<dynamic> records = [];
  bool isLoading = true;

  @override
  void initState() {
    super.initState();
    _fetchHistory();
  }

  Future<void> _fetchHistory() async {
    setState(() => isLoading = true);

    try {
      final response = await http.get(
        Uri.parse("http://$baseURL/attendance/session/${widget.sessionId}"),
      );

      if (response.statusCode == 200) {
        final List data = jsonDecode(response.body);

        // Filter only records for this student
        final filtered = data.where(
              (entry) => entry["student_id"] == widget.studentId,
        ).toList();

        setState(() {
          records = filtered;
          isLoading = false;
        });
      } else {
        setState(() => isLoading = false);
      }
    } catch (e) {
      setState(() => isLoading = false);
    }
  }

  Future<void> _clearHistory() async {
    // You must create a DELETE API in Flask for this.
    // Example endpoint: DELETE /attendance/clear/<student_id>

    try {
      final response = await http.delete(
        Uri.parse("http://$baseURL/attendance/clear/${widget.studentId}"),
      );

      if (response.statusCode == 200) {
        setState(() => records = []);
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text("Attendance history cleared!")),
        );
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text("Server error: ${response.statusCode}")),
        );
      }
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("Network error: $e")),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title:
        const Text("Attendance History", style: TextStyle(color: Colors.black)),
        backgroundColor: Colors.transparent,
        elevation: 0,
        iconTheme: const IconThemeData(color: Colors.black),
      ),
      backgroundColor: Colors.white,
      body: Column(
        children: [
          Expanded(
            child: isLoading
                ? const Center(child: CircularProgressIndicator())
                : records.isEmpty
                ? const Center(child: Text("No attendance records found."))
                : ListView.builder(
              itemCount: records.length,
              itemBuilder: (context, index) {
                final row = records[index];

                return Card(
                  margin: const EdgeInsets.symmetric(
                      horizontal: 20, vertical: 10),
                  color: Colors.teal[50],
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(20),
                  ),
                  child: ListTile(
                    title: const Text(
                      "Attendance Log",
                      style: TextStyle(fontWeight: FontWeight.bold),
                    ),
                    subtitle: Text(
                      "MAC: ${row['mac']}\n"
                          "Time: ${row['timestamp']}\n"
                          "Status: ${row['status']}",
                    ),
                    trailing: Icon(
                      row['status'] == 'Heartbeat'
                          ? Icons.check_circle
                          : Icons.info,
                      color: row['status'] == 'Heartbeat'
                          ? Colors.green
                          : Colors.red,
                    ),
                  ),
                );
              },
            ),
          ),
          TextButton(
            onPressed: _clearHistory,
            style: TextButton.styleFrom(
              foregroundColor: Colors.red,
              textStyle: const TextStyle(fontSize: 14),
            ),
            child: const Text("Clear History"),
          ),
          const SizedBox(height: 10),
        ],
      ),
    );
  }
}
