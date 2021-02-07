const express = require('express');
const helmet = require("helmet");
const {nanoid} = require('nanoid');
const bodyParser = require('body-parser');
const { json } = require('body-parser');
var sqlite3 = require('sqlite3').verbose();

const app = express();

const port = 4545;
const baseURL = `http://localhost:${port}`;

app.use(helmet());
app.use(bodyParser.json());

// ** ENSURE db file is exists otherwise create new file
const db = new sqlite3.Database('./app.db', sqlite3.OPEN_READWRITE | sqlite3.OPEN_CREATE, (err) => {
    if (err) {
        console.error(err.message);
    }

    console.log('Connected to the database.');
});

// ** ENSURE to create table shorturl if not exists
db.serialize(() => {
    db.run('CREATE TABLE IF NOT EXISTS shorturl(id text not null primary key, originalURL text not null)');
});

// ** DISPLAY available URL
app.get('/', (req, res) => {
    res.json({
        url_list: [
            {
                url: '/info',
                method: 'GET',
                params: '',
                body: '',
                desc: 'Shows all data from database'
            },
            {
                url: '/shortenurl',
                method: 'POST',
                params: '',
                body: '{url: "YOUR_STRING_URL"}',
                desc: 'Generates new short url from original url'
            },
            {
                url: '/go/:id',
                method: 'GET',
                params: ':id => the shorten url id',
                body: '',
                desc: 'Access your ORIGINAL Url and redirect to the page'
            }
        ]
    });
})

// ** SHOW all shorturl datas
app.get('/info', async (req, res) => {
    try {
        const response = await new Promise((resolve, reject) => {
            db.all(`SELECT * FROM shorturl`, (err, rows) => {
                if(err) {
                    reject(err);
                }
    
                resolve(rows);
            });
        });

        const results = [];
        for(var row of response) {
            results.push({
                originalURL: row.originalURL,
                shortURL: `${baseURL}/go/${row.id}`
            })
        }

        res.json(results);
    } catch(err) {
        res.status(500).json({message: 'Failed to handle your request'});
    }
    
});
 
// ** GENERATE new url to be shorten
app.post('/shortenurl', async (req, res) => {
    const {url} = req.body;
    if(!url) {
        res.status(404).json('Invalid request');
        return;
    }

    try {
        const newID = nanoid(10);

        const response = await new Promise((resolve, reject) => {
            db.run('INSERT INTO shorturl(id, originalURL) VALUES (?, ?)', [newID, url], err => {
                if(err) {
                    reject(err);
                }
        
                resolve(true);
            });
        });

        if(response) {
            res.status(201).json({
                originalURL: url,
                shortURL: `${baseURL}/go/${newID}`
            });
        }
    } catch(err) {
        res.status(500).json({message: 'Failed to handle your request'});
    }
});

// ** ACCESS shortenurl and redirect to ORIGINAL URL
app.get('/go/:id', async (req, res) => {
    const paramId = req.params['id'];
    if(!paramId) {
        res.status(404).json('Invalid request');
        return;
    }

    try {
        const response = await new Promise((resolve, reject) => {
            db.get(`SELECT * FROM shorturl WHERE id='${paramId}'`, (err, row) => {
            if(err || !row) {
                reject();
            }
    
            resolve(row) 
            });
        }); 
    
        res.redirect(response.originalURL);
    }catch(err) {
        res.status(404).json({message: 'Data was not found'});
    }
});

app.listen(port, () => {
    console.log(`App is running at http://localhost:${port}`);
})
 
