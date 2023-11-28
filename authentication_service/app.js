
const express = require('express')
const app = express()
const port = 3000

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

const ADMIN_USER = "ADMIN"
const ADMIN_PASS = "b03ddf3ca2e714a6548e7495e2a03f5e824eaac9837cd7f159c67b90fb4b7342"

app.get('/', (req, res) => {
  res.send('Hello World!')
})

// process url parameter
app.param('name', function(req, res, next, name) {
    const modified = name.toUpperCase();
  
    req.name = modified;
    next();
  });


// return the hash of the username
app.get('/api/users/:name', function(req, res) {
    if (req.name === "ADMIN") {
        res.send({
            "user_hash": ADMIN_PASS
        })
    }
});
  
  
// create user
app.post('/api/users', function(req, res) {
    const user_id = req.query.id;
    const token = req.query.token;
    const geo = req.query.geo;
  
    res.send({
      'user_id': user_id,
      'token': token,
      'geo': geo
    });
  });

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`)
})
