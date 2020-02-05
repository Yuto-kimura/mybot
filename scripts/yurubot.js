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
    const text = res.message.roomUsers.map(user => `${user.name} ${user.email} ${user.profile_url}`).join('\n\n');
    res.send(text);
  });

  robot.respond(/ROOMID$/i, (res) => {
    res.send(`This room id is ${res.message.room}`);

  });

  robot.respond(/ユーザー登録,(.*)/, (res) => {
    var ID = res.message.room;
    var Name = 'abcde'; // ダミー
    // NEWUSER
    var request = require('/Users/matsumotohiroki/.nodebrew/node/v8.16.1/lib/node_modules/request');
    var options = {
      url: 'http://127.0.0.1:5000/yurubot/api/post',
      method: 'POST',
      headers: {
        "Content-type": "application/json",
      },
      json: {
        'ID':ID,
        'USER_NAME':res.message.user.name,
        'REQUEST':"NEWUSER",
        'KEYWORD':['daab']
      }
    }
    request(options, function (error, response, body) {
      var result = body.data;
    })
 });

  robot.respond(/キーワード送信,(.*)/, (res) => { //送りっぱなしのもの
    var input = res.match[1].split(",");
    var Message = input[1];
    var Keyword = input[0];

    var request = require('/Users/matsumotohiroki/.nodebrew/node/v8.16.1/lib/node_modules/request');
    var options = {
      url: 'http://127.0.0.1:5000/yurubot/api/post',
      method: 'POST',
      headers: {
        "Content-type": "application/json",
      },
      json: {
        'ID':ID,
        'USER_NAME':res.message.user.name,
        'REQUEST':"GET",
        'KEYWORD':keywords
      }
    }
    request(options, function (error, response, body) {
      var Sendlist = body.data; // GET
      Message = '送信者:' + res.message.user.name + '\n' + 'キーワード:' + Keyword + '\n' + Message;

      sendslist(SendList,Message);
    })
  });

  robot.respond(/キーワード質問,(.*)/, (res) => { //解答を待つ送信
    var input = res.match[1].split(",");
    var Message = input[1];
    var Keyword = input[0];
    var ID = res.message.room;
    var request = require('/Users/matsumotohiroki/.nodebrew/node/v8.16.1/lib/node_modules/request');
    var options = {
      url: 'http://127.0.0.1:5000/yurubot/api/post',
      method: 'POST',
      headers: {
        "Content-type": "application/json",
      },
      json: {
        'ID':ID,
        'USER_NAME':res.message.user.name,
        'REQUEST':"GET",
        'KEYWORD':keywords
      }
    }
    request(options, function (error, response, body) {
      var Sendlist = body.data; // GET
      Message = '送信者:' + res.message.user.name + '\n' + 'キーワード:' + Keyword + '\n' + Message;

      sendslist(SendList,Message);

      var date = new Date().toLocaleString('ja-JP', {era:'long'});
      var time =  date.toString();
      tasklist[ID] = [Keyword,time];
    })
  });

  robot.respond(/キーワード確認$/i, (res) => {
    var ID = res.message.room;
    var request = require('/Users/matsumotohiroki/.nodebrew/node/v8.16.1/lib/node_modules/request');
    var options = {
      url: 'http://127.0.0.1:5000/yurubot/api/post',
      method: 'POST',
      headers: {
        "Content-type": "application/json",
      },
      json: {
        'ID':ID,
        'USER_NAME':res.message.user.name,
        'REQUEST':"CHECK",
        'KEYWORD':keywords
      }
    }
    request(options, function (error, response, body) {
      var keywords = body.data; // CHECK
      var keywords_len = keywords.length;
      var ret = '';
      for(var I = 0; I < keywords_len; I++){
          if (I == 0) ret = keywords[I];
          else ret = ret + ', ' + keywords[I];
      }
      res.send(ret);
    })
  });

  robot.respond(/キーワード追加,(.*)/, (res) => {
    var ID = res.message.room;
    var keywords = res.match[1].split(",");
    var request = require('/Users/matsumotohiroki/.nodebrew/node/v8.16.1/lib/node_modules/request');
    var options = {
      url: 'http://127.0.0.1:5000/yurubot/api/post',
      method: 'POST',
      headers: {
        "Content-type": "application/json",
      },
      json: {
        'ID':ID,
        'USER_NAME':res.message.user.name,
        'REQUEST':"CHECK",
        'KEYWORD':keywords
      }
    }
    request(options, function (error, response, body) {
      var nowkeywords = body.data;
      var addkeywords = duplicate_remove_foradd(nowkeywords,keywords);
      var addkeywords_len = addkeywords.length;
      var add_request = {
        'ID':ID,
        'USER_NAME':res.message.user.name,
        'REQUEST':"ADD",
        'KEYWORD':addkeywords
      }
      // ADD
      requestAPI(add_request)

      var ret = '';
      for(var I = 0; I < addkeywords_len; I++){
          if (I == 0) ret = addkeywords[I];
          else ret = ret + ', ' + keywords[I];
      }
      res.send(ret + 'を追加しました');
    })
  });

  robot.respond(/キーワード消去,(.*)/, (res) => {
  // robot.respond(/キーワード追加,(.*)/, (res) => {
    var ID = res.message.room;
    var keywords = res.match[1].split(",");

    var dell_request = {
      'ID':ID,
      'USER_NAME':res.message.user.name,
      'REQUEST':"DELETE",
      'KEYWORD':keywords
    }
    requestAPI(dell_request)

    var keywords_len = keywords.length;
    var ret = '';
    for(var I = 0; I < keywords_len; I++){
        if (I == 0) ret = keywords[I];
        else ret = ret + ', ' + keywords[I];
    }
    res.send(ret + 'を消去しました');
  });

  robot.respond(/しめきり$/i, (res) => {
    var ID = res.message.room;
    //res.send(ID);
    if (tasklist[ID]){
      var Keyword = tasklist[ID][0];
      var time = tasklist[ID][1];
      res.send(time + 'の質問を締め切りました．');
      delete tasklist[ID];
    }else{
      res.send('現在質問をしていません．')
    }

  });

  robot.respond(/HELP$/, (res) => {
    res.send('・ユーザー登録\
    \nユーザーを新規登録します．');

    res.send('・キーワード送信,[keyword],[メッセージ分]\
    \n指定したキーワードを持つ人にメッセージを送信します．その際，指定したキーワードが公開されます．');

    res.send('・キーワード質問,[keyword],[メッセージ分]\
    \n指定したキーワードを持つ人に質問を送信します．「キーワード送信」と異なるところは，「しめきり」で再び同じように質問を締め切ったメッセージが送信できます．');

    res.send('・しめきり\
    \n「キーワード質問」を締め切ります．対象だった人に「締め切りました」というメッセージが送られます．');

    res.send('キーワード追加,[keyword1],[keyword2],...\
    \n自身のキーワードを追加します．追加したいキーワードを,区切りで入力することで同時に複数追加できます．');

    res.send('・キーワード消去,[keyword1],[keyword2],...\
    \n自身のキーワードを消去します．消去したいキーワードを,区切りで入力することで同時に複数消去できます．');

    res.send('キーワード確認\
    \n現在登録されている自分のキーワードを表示します．');
  });


  robot.respond(/help$/, (res) => {
    res.send('・ユーザー登録\
    \n・キーワード送信,[keyword],[メッセージ文]\
    \n・キーワード質問,[keyword],[メッセージ文]\
    \n・しめきり\
    \n・キーワード追加,[keyword1],[keyword2],...\
    \n・キーワード消去,[keyword1],[keyword2],...\
    \n・キーワード確認');
  });


  function requestAPI(json_data){
    var request = require('/Users/matsumotohiroki/.nodebrew/node/v8.16.1/lib/node_modules/request');
    var options = {
      url: 'http://127.0.0.1:5000/yurubot/api/post',
      method: 'POST',
      headers: {
        "Content-type": "application/json",
      },
      json: json_data
    }
    request(options, function (error, response, body) {
      return body.data;
    })
  }


  function sendslist(L,Message){
    var LLength = L.length;
    for(var I = 0;I < LLength; I++){
      robot.send({room : L[I]}, Message);
    }
  }

  function duplicate_remove_foradd(S,A){
    // S .. now status
    // A .. add data

    var SSet = new Set(S);
    var ASet = new Set(A);
    var Ret = new Array;
    for (let a of ASet.values()) {
      if (!SSet.has(a)){
        Ret.push(a);
      }
    }

    return Ret;
  }

};
