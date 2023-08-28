# Yannie Wu, ylw4sj
# CS 3710 Homework: Fuzzing

import aiohttp, asyncio, args, json

async def fuzz(args):
    """Fuzz a target URL with the command-line arguments specified by ``args``."""

    # Create url list
    url_list = []
    f = open(args.wordlist , "r")   
    while True:                         # Read word list
        line = f.readline().strip()
        if line:
            url_list.append(args.url.replace('FUZZ', line)) 
            for e in args.extensions:        # Add extension(s)
                url_list.append(args.url.replace('FUZZ', line+e)) 
        else:
            break
    f.close()

    # Reformat headers to be a dictionary
    headers = {}
    for h in args.headers:
        name, value = h.split(':')
        headers[name] = value

    # Reformat data to be a dictionary
    # data = None
    # if args.data != None:
    #     data = json.loads(args.data)

    # asynchronous loading of a URL:
    async with aiohttp.ClientSession() as session:
        for url in url_list:
            async with session.request(args.method, url, data=args.data, headers=headers) as response:
                #await response.text()
                if response.status in args.match_codes:
                    print(str(response.status) + " " + url)

# do not modify this!
if __name__ == "__main__":
    arguments = args.parse_args()
    asyncio.run(fuzz(arguments))
