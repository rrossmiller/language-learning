import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.io.IOException;

public class NewHttp {
    public static void main(String[] args) {
        // Create an HttpClient instance
        HttpClient client = HttpClient.newHttpClient();

        // Define the URL you want to send the GET request to
        String url = "https://jsonplaceholder.typicode.com/posts/1"; // Replace with your desired URL

        // Create an HttpRequest for the GET request
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(url))
                .build();

        try {
            // Send the GET request and get the response
            HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());

            // Access the response status code and body
            int statusCode = response.statusCode();
            String responseBody = response.body();

            System.out.println("Response Code: " + statusCode);
            System.out.println("Response Body:\n" + responseBody);

            // Access response headers if needed
            // HttpHeaders headers = response.headers();
            // headers.map().forEach((k, v) -> System.out.println(k + ": " + v));

        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
        }
    }
}
