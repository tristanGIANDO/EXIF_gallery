import os
from datalens import envs

ICONS = envs.Icons()

def create_website(paths:list[str], delivery_path:str,
                   user:list[str]=None, overlays:str=None,
                   albums:list[str]=["Home"], website_name:str="datalens_portfolio"):
    """
    file_path (str): the source file
    delivery_path (str): the destination folder where to write HTML file.
    """
    title = "My portfolio"
    subtitle = "Powered by Datalens"
    thumbnail = ICONS.get("logo")

    if len(user) >= 3:
        title = f"{user[1]} {user[2]}" # first name + last name
    if len(user) >= 4:
        subtitle = user[3]
    if len(user) >= 5:
        thumbnail = user[4]

    html_content = f'''
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" href={ICONS.get("logo")} type="image/x-icon">\n
    <title>{title} portfolio</title>\n
    '''

    html_content += '''
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 0;
            background-color: rgb(34, 34, 34);
            color: white;
        }
        header {
            padding: 10px;
            text-align: center;
            background-color: rgb(34, 34, 34);
        }
        .circle {
            width: 150px;
            height: 150px;
            border-radius: 50%;
            overflow: hidden;
            margin: 0 auto;
            display: flex;
            justify-content: center;
            align-items: center;
            background-color: #f0f0f0;
        }
        .circle img {
            max-width: 100%;
            max-height: 100%;
            object-fit: cover;
        }
        nav {
            background-color: #4e4e4e;
            color: #ffffff;
            padding: 10px;
            text-align: center;
        }
        nav a {
            color: #ffffff;
            text-decoration: none;
            margin: 0 10px;
        }
        h2 {
            color: #197092
        }
        .image-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 10px;
            /* position: relative;
            overflow: hidden; */
        }
        .image-item {
            width: 100%;
            padding-bottom: 100%;
            box-sizing: border-box;
            position: relative;
            overflow: hidden;
        }
        .image-item img {
            position: absolute;
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
        .overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.5);
            display: none;
            border-radius: inherit;
            z-index: 1;
        }
        .image-item:hover .overlay {
            display: block;
        }
        .overlay-text {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            text-align: center;
            color: white;
            font-size: 16px;
            z-index: 2;
        }
        footer {
            background-color: #4e4e4e;
            padding: 10px;
            text-align: center;
        }
    </style>
</head>
<body>
    <header>
        <div class="circle">\n
    '''
    html_content += f'''
            <img src="{thumbnail}" alt="Thumbnail">
        </div>
        <h1>{title}</h1>
        <h2>{subtitle}</h2>\n
    </header>
    <nav>\n
    '''

    html_content += '''
    </nav>
    <div class="image-grid">\n
    '''
    for path, overlay in zip(paths,overlays):
        html_content += f'''
        <div class="image-item">
            <img src="{path}" alt="{path}">
            <div class="overlay">
                <div class="overlay-text">
                    {overlay}
                </div>
            </div>
        </div>\n
        '''

    html_content += '''
    </div>
<footer>
        <p>Powered by DataLens</p>
    </footer>
</body>
</html>
'''

    html_file = os.path.join(delivery_path, f"{website_name}.html")

    with open(html_file, "w") as f:
        f.write(html_content)

    return html_file