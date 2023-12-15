  const {Storage} = require('@google-cloud/storage');

  const creds = { // ENV variables
  }

  const storage = new Storage({
    credentials: creds
  });

  const bucketName = 'my-test-bucket-5s';
  const filename = 'background.jpg';
  const expiresTime = 15; //minutes
  const options = {
    version: "v4",
    action: "read",
    expires: Date.now() + expiresTime * 60 * 1000
  }

  function getData() {
    return storage.bucket(bucketName).file(filename).getSignedUrl(options).then(url => {return url})
  }

  let url = getData()
  url.then(function(result) {
    console.log(result)
  })