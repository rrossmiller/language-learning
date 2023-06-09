import java.time.Duration;
import java.time.Instant;

class Fib{
    public static void main(String[] args){
        int ttl=45;
        int[] ans = new int[ttl];
        Instant start = Instant.now();
        ans[0] = 1;
        ans[1] = 1;

        for(int i = 2; i < ans.length; i++){
            ans[i] = ans[i-1] + ans[i-2];
        }
        
        System.out.println(Duration.between(Instant.now(), start).toNanos()*-1);

        for(int i = 0; i < ans.length; i++){
            System.out.println(ans[i]);
        }       
    }
}
