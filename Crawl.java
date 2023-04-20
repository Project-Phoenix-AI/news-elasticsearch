import java.io.IOException;  
import org.jsoup.nodes.Document;
import org.jsoup.Connection;
import org.jsoup.Connection.Response;
import org.jsoup.Jsoup;


public class FirstJsoupExample{  
    public static void main( String[] args ) throws IOException{  
                Document doc = Jsoup.connect("http://www.javatpoint.com").get();  
                String title = doc.title();  
                System.out.println("title is: " + title);  
    }  
}  