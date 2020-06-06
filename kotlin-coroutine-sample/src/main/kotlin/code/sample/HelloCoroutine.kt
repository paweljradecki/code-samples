package code.sample

import kotlinx.coroutines.*
import java.util.concurrent.atomic.AtomicLong
import kotlin.concurrent.thread

/**
    "One can think of a coroutine as a light-weight thread.
    Like threads, coroutines can run in parallel, wait for each other
    and communicate. The biggest difference is that coroutines are very
    cheap, almost free: we can create thousands of them,
    and pay very little in terms of performance.
    True threads, on the other hand, are expensive to start and keep around.
    A thousand threads can be a serious challenge for a modern machine."

    @see https://kotlinlang.org/docs/tutorials/coroutines/coroutines-basic-jvm.html
    @see https://play.kotlinlang.org/#eyJ2ZXJzaW9uIjoiMS4zLjMwIiwicGxhdGZvcm0iOiJqYXZhIiwiYXJncyI6IiIsImNvZGUiOiJpbXBvcnQga290bGlueC5jb3JvdXRpbmVzLipcblxuc3VzcGVuZCBmdW4gbWFpbigpID0gY29yb3V0aW5lU2NvcGUge1xuICAgIGxhdW5jaCB7IFxuICAgICAgIGRlbGF5KDEwMDApXG4gICAgICAgcHJpbnRsbihcIktvdGxpbiBDb3JvdXRpbmVzIFdvcmxkIVwiKSBcbiAgICB9XG4gICAgcHJpbnRsbihcIkhlbGxvXCIpXG59In0=

    Global.launch - start a coroutine
    Global.async - start a coroutine, result as deferred
    deferred.wait - wait for result
 */
fun main() {
    coroutineTest()
//    startLotsOfThreads() // takes too long time!
//    startLotsOfCoroutines() // some coroutines don't finish before main
//    startLotsOfCoroutinesWaitUntilComplete()
//    startCoroutineExecutingSuspendableFunction()
}

private fun coroutineTest() {
    println("Start main")

    // Start a coroutine
    GlobalScope.launch {
        println("Start coroutine")
        delay(1000)
        println("End coroutine")
    }

    // Thread.sleep(2000) // wait for 2 seconds
    // alternative to above...
    runBlocking {
        // blocks until it's done
        delay(2000)
    }
    println("End main")
}

private fun startLotsOfThreads() {
    val c = AtomicLong()
    c.set(0)

    for (i in 1..100_000L) {
        thread(start = true) {
            c.addAndGet(1)
        }
    }
    // sometimes there's need to wait until last addAndGet completes
    println(c)
}

private fun startLotsOfCoroutines() {
    val c1 = AtomicLong()

    for (i in 1..1_000_000L)
        GlobalScope.launch {
            c1.addAndGet(1)
        }

    println(c1.get())
}

private fun startLotsOfCoroutinesWaitUntilComplete() {
    val deferred = (1..1_000_000).map { _ ->
        // async returns deferred which is like future for coroutine
        // map returns result of a function in block, here: deferred
        GlobalScope.async {
            delay(1000)
            1
        }
    }
    // takes 3s to display sum on my machine
    runBlocking {
        val sum = deferred.map {
            it.await().toLong()
        }.sum()
        println("Sum: $sum")
    }
}

/**
 * The biggest merit of coroutines is that they can suspend without
 * blocking a thread. The compiler has to emit some special code to
 * make this possible, so we have to mark functions that may suspend
 * explicitly in the code. We use the suspend modifier for it:
 */
suspend fun workload(n: Int): Int {
    delay(1000)
    return n
}

private fun startCoroutineExecutingSuspendableFunction() {
    GlobalScope.async {
        workload(1_000_000)
    }
}
