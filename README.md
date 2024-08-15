<h1>DB-M</h1>

DB-M A Database and Management tool bringing together technologies like docker, PostgreSQL, Flask and php to serve a database, a backend and a php web interface all in one machine yet in isolate enviroments.
<p></p>
<img src="https://github.com/user-attachments/assets/ef8c2088-8dd4-4ba3-90a6-d5fa1f5ce468" width="705" height="300">


<p></p>
Users can access it via Postman or any other tool to make requests, post data or delete data. As well as upload csv files via html to deploy large amounts of input within seconds into the database.

<h2>Installation</h2>
<p>The only neccessary installation would be the <b>docker engine</b>.</p>
<h3>For Linux</h3>
<code>sudo dnf install docker</code>

after installation, and pulling the code into your desired directory:

<h3>First way of running</h3>
<code>docker compose build</code>
to build your docker containers, and
<code>docker compose up</code>
to run your containers.

<h3>Second way</h3>

<code>docker compose -d up</code>
to run in background. keep in mind that you have to type 
<code>docker compose down</code>
in your command line to shut down your service. Otherwise it will keep running.

You can access to the web interface through <code>localhost:5000/</code>. 

After successfully accessing the web gateway, you can send requests through <bold>csv</bold> files. 

However, if you want to use <i>Postman</i> or any other request maker tool:

<code>GET localhost:4000/users</code> to get all users

<code>POST localhost:4000/users</code> to create user

<code>DELETE localhost:4000/users/user_id</code> to delete a user

<h2>Hope it helps!</h2>
