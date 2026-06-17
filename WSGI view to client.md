**How HTTP request travels from WSGI to View to Client**

A Client (browser) can send a raw request over the internet because a user clicked a button or loaded a URL. This raw data hits the server.


The WSGI server catches these raw internet network packets. It instantly translates them into a neat Python object called an HttpRequest. This object contains everything about the user, including their IP address, what browser they are using, and what URL they are trying to access.


Before reaching view, WSGI pushes this HttpRequest down a line of checkpoints called Middleware. They perfrom multiple security or logging operations. For instance: IF LOGGED_IN == True, or starts a timer to track session. This steps are done in the middle of sending request thus being refered to as middleware.


Once it clears the line of checkpoints, Django looks at the requested URL path and routes the data to the correct View. The View runs the Python code, communicates with a database, and packages everything up into a completed HttpResponse object (the final web page data).


After processing, The direction now flips completely and mirrors almost the same path. The finished response travels backward, climbing back up through the middleware guards. This is  where custom logging code wakes up: in case of our established middleware, it stops the stopwatch, calculates how many milliseconds the view took to run, reads the client's IP from the request metadata, and writes those diagnostics out to your request_metrics.log file.


Then the response hits the WSGI layer one last time. WSGI translates the Python response object back into raw, standardized network byte streams and flushes them across the network socket directly back to the Client's browser, which renders the webpage on the screen.