from django.test import TestCase
from django.urls import reverse


class DashboardViewTest(TestCase):
    def test_dashboard_with_histogram_image(self):
        # Assuming the URL name for the dashboard view is 'dashboard'
        url = reverse('dashboard')
        
        # Make a GET request to the dashboard view
        response = self.client.get(url)
        
        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
        
        # Check that the histogram image is present in the response content
        self.assertIn(b'<img src="/static/histogram_chart.png" alt="Histogram">', response.content)
