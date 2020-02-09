(function () {
    let url = 'http://127.0.0.1:8000/client_server/';
    $('#submit').on('click', function (e) {
        e.preventDefault();
        let usrnam = $('#username').val();
        let pswrd = $('#password').val();
        let user = {
            "type": "login",
            "username": usrnam,
            "password": pswrd
        };
        checkUser(user);
    });

    async function checkUser(user) {
        const response = await fetch(url,{
            method: "POST",
            body: JSON.stringify(user)
        });
        let groups = await response.json();
        if (groups.correct) {
            //console.log(groups);
            startAdmin(groups);
        } else {
            $('.error').removeClass('hidden');
        }
    }
    function startAdmin(groups) {
        $('.wrapper').remove();
        $('#content').html(groups.html);
        addGroups(groups.val);
        $('#request').on('click', async function (e) {
            e.preventDefault();
            let contextTextarea = $('#textarea').val();
            let groupName = $('#list').val()
            let data = {
                "type":'postNewMessage',
                "group":groupName,
                "content":contextTextarea
            }
            const response = await fetch(url, {
                method: "POST",
                body: JSON.stringify(data)
            })
            console.log(await response.json())
        })
    }
    function addGroups(values) {
        console.log(values);
        let list = "<option selected='selected'>" + values[0] + "</option>";
        for (let i = 1; i < values.length; i++) {
            list += "<option>" + values[i] + "</option>"
        }
        $('#list').html(list);
    }
})();



