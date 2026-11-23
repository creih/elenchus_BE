# COMPLEXITY

my greatest takeaway from chapter 2 of the OusterHout' s `philosophy of software design` were
    - what is complexity and its causes
        Obscurity: unclearly defined objects or files that are not capable of clearly and simply showing what they are doing in the code base and why developers used them.
        Dependencies: creating files, objects or simply variables that rely on the existance of others in other to be valid and usefull.
    - How to tell your codebase has complexity:
        . unknown unknowns: code base can't clearly illustrate the code in need of change or what pre-requisites should be known to make the changes.
        . high cognitive load: developer must pass through many files to be able to understand how certain parts work together and be able to do some changes.
        . change amplification: now this is in my understanding the most frustrating, having to change one simple thing but end up re doing it in multiple places within your codebase.

Though I have to agree i can't fully grasp the difference between unkown unknowns and high cognitive load as some scenarios i think of end up being both at the same time,
so clearly distinguishing them has not yet fully clicked.

Also I up till now though that complexity was only about the way a system uses resources( O notations with regards to time and space) and how fast it can get a task done never had i thought of it in terms of code readabilty and refactoring in terms of amelioration or simply adding new changes to it.


# HTTP Story

About the http i mostly retained that it was originally built on top of TCP in order to allow the requesting and receiveing of cleanily and specifically formated data like hypertexts as http only did allow the passing of raw bytes from computer to computer and as he had just made the world wide web he must have needed a way to service his newly created invention and instead of seeing tcp as an obstacle used it as a bridge.

Then later on with new demands for the forms of data and other users' and developers' needs http was improved to http/0.9, http/1.1 and later on http/2 to accomodate things like using headers and status code, keep alive connections, and multiplexing.