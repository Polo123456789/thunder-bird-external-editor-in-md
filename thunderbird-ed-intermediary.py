#!/bin/python3

# {{{
# Example eml file
# 
# From: Pablo Sanchez Galdamez <pablo.san@eukanuba-gt.com>
# To: Ecwid Help Center <ec.customizations@lightspeedhq.com>
# Cc: 
# Bcc: 
# Reply-To: 
# Subject: Re: New customization request for Store ID 29462425
# X-ExtEditorR-Send-On-Exit: false
# X-ExtEditorR-Help: Use one address per `To/Cc/Bcc/Reply-To` header
# X-ExtEditorR-Help: (e.g. two recipients require two `To:` headers).
# X-ExtEditorR-Help: KEEP blank line below to separate headers from body.
# 
# <!DOCTYPE html>
# <html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"></head><body><p><br></p><pre class="moz-signature" cols="72">Pablo Sanchez
# Benisa S.A</pre><div class="moz-cite-prefix">On 31/10/23 07:41, Ecwid Help Center wrote:<br></div><blockquote type="cite" cite="mid:15VNJ79VVND_6541040fcd6f9_4146b411541b4_sprut@zendesk.com">
# 
# 	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
# 	<link href="https://fonts.googleapis.com/css?family=Open+Sans;300,400,600,700&amp;:subset=cyrillic,latin" rel="stylesheet" type="text/css">
# 	<style type="text/css">table td {
# 			border-collapse: collapse;
# 		}a, a:hover {
# 			color: #1278C1 !important;
# 			text-decoration: none !important;
# 		}p {
# 			color: #333 !important;
# 			font-family: 'Open Sans',sans-serif !important;
# 			font-size: 14px !important;
# 			line-height: 24px !important;
# 			margin: 0 !important;
# 			padding: 0 0 16px !important;
# 		}body[dir=rtl] .directional_text_wrapper { direction: rtl; unicode-bidi: embed; }</style>
# 
# 
# 	<div style="font-family: 'Open Sans',sans-serif;font-size: 14px;line-height: 24px;padding: 0;color: #333;">
# 		<div style="color: #ffffff;font-size: 0;line-height: 0;">##- Please type your reply above this line -##</div>
# 			 
# 			<div style="margin-top: 25px" data-version="2"><table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0">  <tbody><tr>    <td style="padding: 15px 0; border-top: 1px dotted #c5c5c5;" width="100%">      <table style="table-layout:fixed;" role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0">        <tbody><tr>                    <td style="padding: 0; margin: 0;" width="100%" valign="top">            <p style="font-family:'Lucida Grande','Lucida Sans Unicode','Lucida Sans',Verdana,Tahoma,sans-serif; font-size: 15px; line-height: 18px; margin-bottom: 0; margin-top: 0; padding: 0; color:#1b1d1e;" dir="ltr">                                                <strong>Anastasia V.</strong> (Ecwid Help Center)                                          </p>            <p style="font-family:'Lucida Grande','Lucida Sans Unicode','Lucida Sans',Verdana,Tahoma,sans-serif; font-size: 13px; line-height: 25px; margin-bottom: 15px; margin-top: 0; padding: 0; color:#bbbbbb;" dir="ltr">              Oct 31, 2023, 17:41 GMT+4            </p>                                    <div class="zd-comment" dir="auto" style="color: #2b2e2f; line-height: 22px; margin: 15px 0">Hi Pablo, <br> <br>Hope you are doing well now! <br> <br>Thank you for sharing links with API keys! Unfortunately, the information was deleted automatically, so I missed my chance to copy it. Could you resend the details? <br> <br>Thank you!<br><div class="signature"><p dir="ltr" style="color: #2b2e2f; line-height: 22px; margin: 15px 0">Best regards,<br>
# Anastasia V.<br>
# Ecwid by Lightspeed Customization Service</p></div></div><p dir="ltr">                      </p></td>        </tr>      </tbody></table>    </td>  </tr></tbody></table></div> 
# 			
# 	</div>
# <span style="color:#FFFFFF" aria-hidden="true">[15VNJ7-9VVND]</span>
# <div itemscope="" itemtype="http://schema.org/EmailMessage" style="display:none">  <div itemprop="action" itemscope="" itemtype="http://schema.org/ViewAction">    <link itemprop="url" href="https://support.ecwid.com/hc/requests/2348357">    <meta itemprop="name" content="View ticket">  </div></div>
# </blockquote></body></html>

# This program will create a temporary markdown file
# That has the headers as a comment in a yaml block:
# ---
# #From: Pablo Sanchez Galdamez <pablo.san@eukanuba-gt.com>
# #To: Ecwid Help Center <ec.customizations@lightspeedhq.com>
# #Cc: 
# #Bcc: 
# #Reply-To: 
# #Subject: Re: New customization request for Store ID 29462425
# #X-ExtEditorR-Send-On-Exit: false
# #X-ExtEditorR-Help: Use one address per `To/Cc/Bcc/Reply-To` header
# #X-ExtEditorR-Help: (e.g. two recipients require two `To:` headers).
# #X-ExtEditorR-Help: KEEP blank line below to separate headers from body.
# ---
#
# And will replace the first <p><br></p> in the body of the email with the
# contents of the markdown file turned into html with pandoc
#
# It will then replace the whole .eml file with a new one, retaining the headers
# but replacing the body with the new html body.
# The markdown file will be deleted, it should be edited with EDITOR before
# sending.
# }}}

import sys
import tempfile
import subprocess
import bs4

EDITOR = "nvim"

def main():
    # Check if $1 is present
    if len(sys.argv) < 2:
        print("No file specified")
        sys.exit(1)

    emailFile = sys.argv[1];
    headers: list[str] = []
    originalBody: list[str] = []

    with open(emailFile) as f:
            lines = f.readlines()
            inBody = False
            for line in lines:
                if len(line.strip()) == 0:
                    inBody = True
                    continue
                if inBody:
                    originalBody.append(line)
                else:
                    headers.append(line)


    # Create a temporary markdown file
    # That has the headers as a comment in a yaml block:
    tmpFile = tempfile.gettempdir() + "/thunderbird-ed-intermediary.md"
    with open(tmpFile, "w") as f:
        f.write("---\n")
        for header in headers:
            f.write("#" + header)
        f.write("---\n")
        f.write("\n")
        f.write("\n")

    
    # Open file with EDITOR
    subprocess.call([EDITOR, tmpFile])

    # Convert markdown to html
    html = subprocess.check_output(["pandoc", tmpFile]).decode("utf-8")

    # Replace first <p><br></p> with html using bs4
    originalBodyText = "".join(originalBody)
    soup = bs4.BeautifulSoup(originalBodyText, "html.parser")
    body = soup.body
    if body is None:
        print("Error parsing html, no body")
        sys.exit(1)
    firstP = body.find("p")
    if firstP is None:
        print("Error parsing html, no first <p>")
        sys.exit(1)
    firstP.replace_with(bs4.BeautifulSoup(html, "html.parser"))

    # Replace the whole .eml file with a new one, retaining the headers
    # but replacing the body with the new html body.
    with open(emailFile, "w") as f:
        for header in headers:
            f.write(header)
        f.write("\n")
        f.write(str(soup))
    
if __name__ == "__main__":
    main()

# vim: set foldmethod=marker:
