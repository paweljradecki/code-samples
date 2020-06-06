package code.sample.http.vertx;

import io.vertx.core.Vertx;

public class JavaVertxSimplestHttpServer {
    /**
     * httperf --port 8082 --num-calls 100000
     * gives
     *
     * Request rate: 17827.1 req/s (0.1 ms/req)
     * Reply status: 1xx=0 2xx=100000 3xx=0 4xx=0 5xx=0
     *
     * CPU time [s]: user 1.05 system 4.11 (user 18.6% system 73.3% total 92.0%)
     * Net I/O: 1967.2 KB/s (16.1*10^6 bps)
     */
    public static void main(String[] args) {
        Vertx.vertx()
            .createHttpServer()
            .requestHandler(req ->
                    req.response().end("Hello World!")
            ).listen(8082);
    }
}
