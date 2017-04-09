function init(){
	obj = new Posts();
	obj.load();
}
Posts = function(){
	/*this.load = function(){
		for(var i=0; i<{{n_blogs}}; i++){
			obj.putcontent("{{head.head[0]}}","{{content.content[0]}}")
		}
	}*/
	this.load = function(){
		{% for i in range(0,n_blogs)%}
			obj.putcontent("{{head.head[i]}}","{{content.content[i]}}")
		{%endfor%}
	}
	this.putcontent = function(head,post){
		panel = document.createElement('div');
		panel.className = "panel panel-default";
		header = document.createElement('div');
		header.className = "panel-heading";
		header.innerHTML = head;
		content = document.createElement('div');
		content.className = "panel-body";
		content.innerHTML = post;
		panel.appendChild(header);
		panel.appendChild(content);
		pgroup = document.getElementById('posts');
		pgroup.appendChild(panel);
	}
	
}