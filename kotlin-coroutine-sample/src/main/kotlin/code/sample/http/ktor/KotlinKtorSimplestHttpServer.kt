package code.sample.http.ktor

import io.ktor.application.*
import io.ktor.http.*
import io.ktor.response.*
import io.ktor.routing.*
import io.ktor.server.engine.*
import io.ktor.server.netty.*

/**
 * httperf --port 8081 --num-calls 100000
 * gives
 *
 * Request rate: 7658.1 req/s (0.1 ms/req)
 * Reply status: 1xx=0 2xx=100000 3xx=0 4xx=0 5xx=0
 *
 * CPU time [s]: user 2.17 system 9.00 (user 16.6% system 68.9% total 85.5%)
 * Net I/O: 1151.7 KB/s (9.4*10^6 bps)
 */
fun main() {
    embeddedServer(Netty, 8081) {
        routing {
            get("/") {
                call.respondText("Hello, world!", ContentType.Text.Html)
            }
        }
    }.start(wait = true)
}

