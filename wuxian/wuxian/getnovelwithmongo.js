
var MongoClient = require('mongodb').MongoClient;
var request = require('request');
var path = require('path'); 
var fs = require('fs');
var Bagpipe = require('bagpipe');


var listUrl=new Array(); 
var filenames=new Array();


var singerList=[]
var page_Num=0;


//连接字符串
//var DB_CONN_STR = {'mongodb://localhost:27017/users':true}
var DB_CONN_STR = 'mongodb://localhost:27017/'
var db='wuxianxiaoshuo'
var dbtables=["奇幻魔法","探险推理","耽美百合","作者合集",
"都市异能","都市生活","军警谍战","武侠小说","网游竞技",
"历史军工","现代异侠","官场商战","热血青春","仙侠修真",
"东方玄幻","灵异奇谈","衍生同人","职场励志","现代修真",
"异世大陆","言情小说","科幻小说",]

dbclient(DB_CONN_STR,'wuxianxiaoshuo',dbtables[3],function(db){
	console.log('client0 connect DB finished ')
	
});
var dbtable=['探险推理']

/*
for(let i in dbtables){

	console.log(dbtables[i])
	mknovelfolder(dbtables[i])
	//dbclient(DB_CONN_STR,'wuxianxiaoshuo','作者合集',function(db){
	//	console.log('client0 connect DB finished ')
	
	//});
}
*/
function mknovelfolder(noveltype){
	var rootfolder= './'+'无限小说'
	var basefolder=rootfolder+'/'+noveltype+'/'

	fs.access(rootfolder, function (err){
			if(err){
				fs.mkdir(rootfolder,function(err){
					
					fs.access(basefolder, function (err){
						if(err){
							
							fs.mkdir(basefolder,function(err){
							
							});
						}
					});	
				});
			}else{
				
				fs.access(basefolder, function (err){
					if(err){
						fs.mkdir(basefolder,function(err){
							
						});
					}
				});	
			}
	});
}




function downloadnovel(url,filename){
	console.log(url,filename)
	request.head(url, function(err, res, body){ 
		if (err) { 
			console.log('err: '+ err); 
			return false; 
		} 

		console.log('正在下载文件[%s]:  写入文件  --------',filename); 
		request(url).pipe(fs.createWriteStream(filename)).on('close',callback); //调用request的管道来下载到 images文件夹下 
		
		function callback(){
			console.log('filename=[%s] 下载完毕',filename)
		}
});

}

function dbclient(host,collections,dbs,callback){
	MongoClient.connect(host, {useNewUrlParser:true},function(err, client) {
		var collect=client.db(collections)
		var db = collect.collection(dbs);
		findAllData(db,function(response){
			console.log('查询结束, response.length = %d',response.length);
			client.close()
			var novelpipe=new Bagpipe(response.length)
			for(let i in response){
				item=response[i];

				novelname=item['novelname'];
				//novelname=novelname.trim().replace(/[\\~`:\[\]?!！《》，/() &*]/g,'');
				novelname=novelname+'.txt';
				novelid=item['novelid'];
				
				txturl = 'http://down.555x.org/txt/'+novelid+'/'+encodeURIComponent(novelname);
				filename=dbs+'\\'+novelname;
				console.log(filename,txturl);
				novelpipe.push(downloadnovel,txturl,filename);
				//downloadnovel(txturl,filename)
			}
		});
		console.log('连接 %s 成功,set collection[%s] and db[%s] finished',host,collections,dbs)
		callback(db)
	});
}

//定义函数表达式，用于操作数据库并返回结果，插入数据
var insertManyData = function(db, data,callback) {  
    db.insertMany(data, function(err, result) { 
    //如果存在错误
        if(err)
        {
            console.log('Error:'+ err);
            return;
        }else{
			//调用传入的回调方法，将操作结果返回
			//console.log(result)
			callback(result);
		}
    });
}

//定义函数表达式，用于操作数据库并返回结果，插入数据
var insertOneData = function(db, data) {  
    db.insertOne(data, function(err, result){ 
        if(err){
			//如果存在错误
            console.log('Error:'+ err);
            return;
        }else{
			console.log('One date be insert finished')
		}
    });
}


//定义函数表达式，用于操作数据库并返回结果，更新数据
var updateKeyData = function(db, olddata,newdata,callback) {  
    //获得指定的集合 

    //要修改数据的条件，>=10岁的用户
    //var  where={age:{"$gte":10}};
    //要修改的结果
	console.log(olddata)
	//console.log(newdata)
    var set={$set:newdata};
    db.updateMany(olddata,set, function(err, result) { 
        //如果存在错误
        if(err)
        {
            console.log('Error:'+ err);
            return;
        }else{
			//调用传入的回调方法，将操作结果返回
			callback(result);
		}    
    });
}

//定义函数表达式，用于操作数据库并返回结果，更新数据
var updateData = function(db, callback) {  
    //获得指定的集合 
    var collection = db.collection('users');
    //要修改数据的条件，>=10岁的用户
    var  where={age:{"$gte":10}};
    //要修改的结果
    var set={$set:{age:95}};
    collection.updateMany(where,set, function(err, result) { 
        //如果存在错误
        if(err)
        {
            console.log('Error:'+ err);
            return;
        } 
        //调用传入的回调方法，将操作结果返回
        callback(result);
    });
}

//定义函数表达式，用于操作数据库并返回结果，从所有数据中获取指定元素数据
var findkeyData = function(db,keyword,callback) {  
	var keyvalue=[]
	var allvalue=[]
    db.find().toArray(function(err, result) { 
        //如果存在错误
        if(err){
            console.log('Error:'+ err);
            return;
        }else{
			result.forEach(function(val){
				for(let item in val){
					console.log(val)
					if(item == keyword){
						//console.log(val[item]);
						//console.log(val);
						keyvalue.push(val[item]);
						allvalue.push(val);
					}	
				}	
			});    
		}
		console.log('get keyvalue list finished');
		//console.log(allvalue);
		callback(keyvalue,allvalue);
    });	
}


//定义函数表达式，用于操作数据库并返回结果，查询数据
var findAllData = function(db,callback) {  
    db.find().toArray(function(err, result) { 
        //如果存在错误
        if(err)
        {
            console.log('Error:'+ err);
            return;
        } 

		console.log(result.length)
        callback(result);
    });
}

//定义函数表达式，用于操作数据库并返回结果，删除数据
var removeData = function(db, callback) {  
    //获得指定的集合 
    var collection = db.collection('users');
    //要删除数据的条件，_id>2的用户删除
    var  where={_id:{"$gt":2}};
    collection.remove(where,function(err, result) { 
        //如果存在错误
        if(err)
        {
            console.log('Error:'+ err);
            return;
        } 
        //调用传入的回调方法，将操作结果返回
        callback(result);
    });
}
