This was largely generated by ChatGPT so that I could have the tool for my mass photo organisation project.

This project was my attempt at trying to compile one easily navigatable folder of photos, videos, audio and documents from all of my phone backups.

It finds all images and places them in the folder of the year and month, the same for all RAW files however these have their own separate folder within the target month.

Any other documents such as PDFs, Powerpoints etc are collected into one large Files folder in the directory containing the years.


The list of files gathered are:

PHOTO_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.heic', '.heif', '.psd', '.svg'}

RAW_EXTENSIONS = {'.raw', '.arw', '.cr2', '.nef', '.orf', '.sr2', '.dng', '.rw2', '.pef', '.srw', '.x3f', '.crw'}

DOCUMENT_EXTENSIONS = {'.pdf', '.txt', '.doc', '.docx', '.odt', '.rtf', '.md', '.html', '.htm', '.xml', '.json', '.csv', '.xls', '.xlsx', '.ppt', '.pptx'}