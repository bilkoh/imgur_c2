
# IMGUR C2
## What is it?
Some scripts to send and receive binaries from a botnet operator to a victim node.

It takes a binary (eg: a reverse shell meterpreter) converts it to an images that can be posted by the operator and easily found by the victim nodes awaiting to download the images, convert them back to binaries, and then execute them. We rely on a binary of your choice to do the actual communication.

## Then it's not a C2?
Maybe. But probably not. Anway, who wants to rename a git repo at this point?

## What is it a solution for?
When you want to slyly set up a line of communication between an operator and a victim. Or when you're transmitting a binary you want to run while hiding it in inocuous traffic like imgur.com, and avoiding sensors in IDS that alert for data like base64 strings of binaries.

Also, traditional botnets often have some kind of reporting server or component that logs and keep tracks of active victim nodes. Since it's easy to block a C2 or reporting server on a fixed address, more advanced botnets are coded with a domain generation algorithm that switches domains at regular intervals to thwart such blocks. IMGUR C2 does something similar by leveraging imgur's tagging system. We have a tag name generation algorithm that the victims nodes watch and wait for uploads

## How do I use it?
1. Convert a binary to an image:
    `python3 cli.py -b evil.exe -o not_evil.png`
2. Upload image under this generated tag. (You will do this manually.) 
Run to find valid tag:
    `python3 cli.py -t`
3. Though bot watches tag for new uploads. 
    You can test an image by converting an image back to a binary:
    `python3 cli.py -i not_evil.png -o evil.exe`

## How do I install it?
`pip install -r requirements.txt `

## Notes:
- Test scripts use standard meterpreter binary, which Windows Virus & Threat Protection will remove if `Real-time Protection` is enabled. You will need to disable this for test script to pass if you're running on Windows.
- I've only tested this on imgur with the `PNG` format.
- Haven't tested a binary larger than 1.12mb.