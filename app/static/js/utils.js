var log = console.log.bind(console);

var show_mansory = function(mansory_obj) {
	mansory_obj.mpmansory({
	  childrenClass: '', // default is a div
	     columnClasses: '', //add classes to items
	     breakpoints:{
	       lg: 3, 
	       md: 4, 
	       sm: 6,
	       xs: 12
	     },
	     distributeBy: { order: false, height: false, attr: 'data-order', attrOrder: '-asc' }, 
	     onload: function (items) {
	       //make somthing with items
	  }
	});
};

var event_hide = function(event){
	
		var self = event.target
		var id = self.id
		// log('target click', self.id)
		if (id.indexOf('hide-') != -1) {
			log('exist')
			hide_post(self.dataset.post, self)
		} else {
			//log('not exist')
		}

}


var hide_post = function(post_id, obj) {
	var id = post_id;
	//log('click', id)
	log('parent obj', obj)
	$.ajax({
		type:'PUT',
		url:'/hide_post/'+id+'/',
		success:function(response){
			log(response);
			var thumbnailParent =  obj.closest('.thumbnail')
			thumbnailParent.remove()
		},
	});

};

var qs = function(query) {
	return document.querySelector(query)
}

