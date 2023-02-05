const { exec } = require('child_process');

exec("/usr/bin/wg-quick up wg0" , ( err , stdout , stderr ) => {
    exec("tail -f /dev/null" , (err , stdout , stderr) => {})
})

