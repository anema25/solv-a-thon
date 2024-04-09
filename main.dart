import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Professor Recommender',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        visualDensity: VisualDensity.adaptivePlatformDensity,
      ),
      home: RecommendationScreen(),
    );
  }
}

class RecommendationScreen extends StatefulWidget {
  @override
  _RecommendationScreenState createState() => _RecommendationScreenState();
}

class _RecommendationScreenState extends State<RecommendationScreen> {
  TextEditingController _interestController = TextEditingController();
  List<dynamic> _recommendedProfessors = [];

  Future<void> _getRecommendations(String interests) async {
    String url = 'http://127.0.0.1:5000/recommend_professors_nlp'; // Update this URL
    Map<String, String> headers = {"Content-type": "application/json"};
    String json = jsonEncode({'interests': interests});

    try {
      final response = await http.post(Uri.parse(url), headers: headers, body: json);
      if (response.statusCode == 200) {
        setState(() {
          _recommendedProfessors = jsonDecode(response.body);
        });
      } else {
        throw Exception('Failed to load recommendations');
      }
    } catch (e) {
      print('Error: $e');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Professor Recommendations'),
      ),
      body: Padding(
        padding: EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            TextField(
              controller: _interestController,
              decoration: InputDecoration(labelText: 'Enter your interests'),
            ),
            SizedBox(height: 20.0),
            ElevatedButton(
              onPressed: () {
                _getRecommendations(_interestController.text);
              },
              child: Text('Get Recommendations'),
            ),
            SizedBox(height: 20.0),
            Expanded(
              child: ListView.builder(
                itemCount: _recommendedProfessors.length,
                itemBuilder: (context, index) {
                  return ListTile(
                    title: Text(_recommendedProfessors[index]['name']),
                    subtitle: Text(_recommendedProfessors[index]['area_of_work']),
                  );
                },
              ),
            ),
          ],
        ),
      ),
    );
  }
}
