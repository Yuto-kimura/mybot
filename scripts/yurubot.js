// Description:
//   Utility commands surrounding Hubot uptime.
//
// Commands:
//   ping - Reply with pong
//   echo <text> - Reply back with <text>
//   time - Reply with current time
'use strict';

var tasklist = {};

module.exports = (robot) => {
  robot.respond(/TEST$/i, (res) => {
    sendslist(['_231478410_897581056','_231493067_1694498816','_231489514_-1723858944'] ,'sendslist test');
  });

  robot.respond(/ROOMID$/i, (res) => {
    res.send(`This room id is ${res.message.room}`);

  });

//   robot.respond(/ユーザー登録$/i, (res) => {
//     var ID = ;
//     var Name = ;
//     var request = new XMLHttpRequest();

//     request.open('GET','https://127.0.0.1:5000/yurubot/api/get',true);
//     request.responseType = 'json';

//     request.onload = function(){
//         var data = this.response;
//         console.log(data);
//     };

//   });

  robot.respond(/キーワード送信$/i, (res) => { //送りっぱなしのもの
    var SendList = [];
    var Message = '';
    var Keywords;

    // getAPI
    SendList = ['_231478410_897581056'];
    Message = '送信者:' + res.message.user.name + '\n';

    sendslist(SendList,Message);
  });

  robot.respond(/キーワード質問$/i, (res) => { //解答を待つ送信
    var ID = res.message.room;
    var SendList = [];
    var Message = '';
    var Keywords;

    // getAPI
    SendList = ['_231478410_897581056'];
    Message = '送信者:' + res.message.user.name + '\n';

    sendslist(SendList,Message);

    var time = 0;
    tasklist[ID] = [Keywords,time]
  });

  robot.respond(/キーワード確認$/i, (res) => {
    var ID = res.message.room;
    var keywords;
    //keyword check
    keywords = ['abc','cde','efg']; //for test
    var keywords_len = keywords.length;
    var ret = '';
    for(var I = 0; I < keywords_len; I++){
        if (I == 0) ret = keywords[I];
        else ret = ret + ', ' + keywords[I];
    }
    res.send(ret);
  });

  robot.respond(/キーワード追加$/i, (res) => {
    var ID = res.message.room;
    var addkeywords;
    //keyword add API
    addkeywords = ['abc','cde','efg']; //for test
    var keywords_len = keywords.length;

    var ret = ''; // keyword check
    for(var I = 0; I < keywords_len; I++){
        if (I == 0) ret = keywords[I];
        else ret = ret + ', ' + keywords[I];
    }
    res.send(ret + 'を追加しました');
  });

  robot.respond(/キーワード消去$/i, (res) => {
    var ID = res.message.room;
    var keywords;
    //keyword delete API
    keywords = ['abc','cde','efg']; //for test
    var keywords_len = keywords.length;
    var ret = '';
    for(var I = 0; I < keywords_len; I++){
        if (I == 0) ret = keywords[I];
        else ret = ret + ', ' + keywords[I];
    }
    res.send(ret + 'を消去しました');
  });

  robot.respond(/しめきり$/i, (res) => {
    
  });

  

  function sendslist(L,Message){
    var LLength = L.length;
    for(var I = 0;I < LLength; I++){
      robot.send({room : L[I]}, Message);
    }
  }
};