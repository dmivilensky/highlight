$('.chips-autocomplete').chips({
    data: [{
        tag: 'Важный',
    }],
    autocompleteOptions: {
        data: {
            'Важный': null,
            'Картинка': null,
        },
        limit: Infinity,
        minLength: 1
    }
});