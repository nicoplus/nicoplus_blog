var show_mansory = function() {
	$('#mansory').mpmansory({
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

var delete_post = function(post_id) {
	var id = post_id;
	$('#delete-'+id).click(function(){
		$.ajax({
			type:'PUT',
			url:'/hide_post/'+id,
			success:function(response){
				log(response);
				window.location.reload();
			},
		});

	});
};