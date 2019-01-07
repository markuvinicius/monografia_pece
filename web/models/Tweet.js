const mongoose = require('mongoose');

const tweetSchema = new mongoose.Schema({    
  data: {
    type: String,    
    trim:true,
  },
  usuario:{
      type:String, 
      trim:true,     
  },       
  texto:{
      type:String,      
      trim:true,
  },
  data:{
      type:String,
      trim:true,
  }, 
  label:{
      type:String,      
  },
  labeled_by:{
      type:mongoose.Schema.Types.ObjectId,
  }   
});

module.exports = mongoose.model('Tweet', tweetSchema);