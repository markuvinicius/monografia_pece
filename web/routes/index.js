const express = require('express');
const mongoose = require('mongoose');
const { body, validationResult } = require('express-validator/check');
const router = express.Router();

//const Registration = mongoose.model('Registration');
const Tweet = mongoose.model('Tweet');

router.get('/', (req, res) => {
    res.render('form', { title: 'Registration form' });
});

router.post('/',
  [
    body('name')
      .isLength({ min: 1 })
      .withMessage('Por favor, informe seu nome'),
    body('email')
      .isLength({ min: 1 })
      .withMessage('Por favor, informe seu e-mail'),
  ],
  (req, res) => {
    const errors = validationResult(req);

    if (errors.isEmpty()) {
        const registration = new Registration(req.body);
        registration.save()
            .then(() => { res.send('Thank you for your registration!'); })
            .catch(() => { res.send('Sorry! Something went wrong.'); });
    } else {
      res.render('form', {
        title: 'Registration form',
        errors: errors.array(),
        data: req.body,
      });
    }
  }
);

router.get('/registrations', (req, res) => {
    Registration.find()
      .then((registrations) => {
        //console.log(registrations)
        res.render('index', { title: 'Listing registrations', registrations });
      })
      .catch(() => { res.send('Sorry! Something went wrong.'); });
});

router.get('/unlabeled', (req,res) => {
    Tweet.find({"label":null}).limit(5)
      .then((tweets) => {        
        res.render('unlabeled', {title: 'Unlabeled Tweets', tweets});
      })
      .catch(() => { res.send('Sorry! Something went wrong.'); });
});

router.post('/save', (req, res) => {
    for(var attributename in req.body){
      //onsole.log(attributename+": "+req.body[attributename]);      
      var id = attributename
      var label = req.body[attributename]            
        
      Tweet.findByIdAndUpdate(id, 
        {"label": label},
        (err, todo) => {
          // Handle any possible database errors
          if (err) 
            return res.status(500).send(err);          
        })
    }
    res.redirect('/unlabeled')            
});

module.exports = router;