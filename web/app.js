const express = require('express');
const session = require('express-session');
const path = require('path');
const routes = require('./routes/index');
const bodyParser = require('body-parser');

const app = express();

app.use(session({secret:'ssshhhhh'}));
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'pug');

app.use(bodyParser.urlencoded({ extended: true }));
app.use('/', routes);
app.use(express.static('public'));

app.post(function(req, res, next){
    next();
});

module.exports = app;