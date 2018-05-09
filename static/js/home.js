 //取图片加菜单
        let shops_url = 'http://127.0.0.1:8000/home/shops/';
        let IMG_URLS = 'http://127.0.0.1:8000/static/img/productSingle_middle/';
        $(function () {

            $.get(shops_url, function (result) {
                if (result != null && result.state === 200 && result.data.length > 0) {
                    let $content = $('#content');
                    for (let cate of result.data) {
                        let $div = $('<div>');
                        let $h3 = $('<h3>').text(cate.name);
                        let $ul = $('<ul>').attr('class', 'clear');
                        if (cate.products.length > 0) {
                            for (let product of cate.products) {
                                let $li = $('<li>');
                                let $a = $('<a>');
                                $a.append($('<img>').attr('src', IMG_URLS + product.imgs[0].id + '.jpg'))
                                    .append($('<br>'))
                                    .append($('<span>').text(product.name))
                                    .append($('<br>'))
                                    .append($('<span>').text(product.promoteprice));
                                $li.append($a);
                                $ul.append($li)
                            }
                        }
                        $('#content').append($div.append($h3).append($ul));
                    }

                }
            })
        });


        //搜索商品信息
        let IMG_URL = 'http://127.0.0.1:8000/static/img/productSingle_middle/';
        //点击搜索
        $(function () {
            $('#search_btn').click(function () {
                let keywords = $('#search_inp').val();
                let search_url = 'http://127.0.0.1:8000/home/search/?key=' + keywords;
                $.getJSON(search_url, function (result) {
                    if (result.state === 200) {
                        let $ul = $('#search_shops');
                        for (let index in result.data) {
                            let product = result.data[index];
                            let $li = $('<li>');
                            $('<img>').attr('src', IMG_URL + product.img_list[0].id + '.jpg').appendTo($li);
                            $('<p>').text('¥' + product.promoteprice).appendTo($li);
                            $('<a>').attr('href', 'product?pid = ' + product.id).text(product.name).appendTo($li);
                            $('<a>').attr('href', 'product?pid = ' + product.id).text('天猫专卖').appendTo($li);
                            $ul.append($li)
                        }
                    } else {

                    }
                })
            })
        });

        //分类菜单加轮播图
        $(function () {
            init();

        });

        function init() {
            load_data();
            init_cate();

            init_banner();


        }

        //初始化
        function load_data() {
            let cate_url = 'http://127.0.0.1:8000/home/cate/';
            let setting = {
                type: 'GET',
                success: function (result) {
                    if (result.state === 200) {
                        init_cate(result.data);
                        init_banner(result.banners)
                    }
                }
            };
            $.ajax(cate_url, setting)
        }

        function init_cate(data) {
            let $cate_ul = $('#cate').mouseout(function () {
                $('.sub').css('display', 'none')
            });
            for (let cate of data) {
                $('<li>').mouseover(function () {
                    let $ul = $('.sub').empty().css('display', 'block');
                    for (let sub of cate.subs) {
                        $('<li>').append($('<a>').text(sub.name)).appendTo($ul)
                    }
                }).append($('<a>').text(cate.name)).appendTo($cate_ul)
            }
        }

        function init_banner(banners) {
            let IMG_URL = 'http://127.0.0.1:8000';
            let $banner_ul = $('.banner>ul');
            for (let banner of banners) {
                $('<li>').append($('<a>').append($('<img>').attr('src', IMG_URL + banner.img))).appendTo($banner_ul)
            }
            lunbo()

        }

        function lunbo() {
            $('.banner').unslider({
                speed: 1000,
                dots: true
            })
        }