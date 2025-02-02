function RemoveFromFavorites(articleId) {
        $.get('/remove-from-favorites?article_id=' + articleId).then(res => {
            if (res.success) {
                $('#favorite-article-' + articleId).remove();
            }
        })
}

