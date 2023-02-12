import aiohttp
import json
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from dotenv import dotenv_values
from typing import List



#
verify_url = 'https://levada-server.onrender.com/login/verifyemail/'
change_password_url = 'https://levada-server.onrender.com/user/changepasword/'

config_credentials = dotenv_values(".env")
#"smtp-relay.sendinblue.com",
conf = ConnectionConfig(
    MAIL_USERNAME = config_credentials["USERNAME"],
    MAIL_PASSWORD = config_credentials["PASS"],
    MAIL_FROM = config_credentials["EMAIL"],
    MAIL_PORT = 587,
    MAIL_SERVER = "in-v3.mailjet.com",
    MAIL_TLS = True,
    MAIL_SSL = False,
    USE_CREDENTIALS = True
)


async def send_email(email: str, linkTo: str, is_verification: bool = True):
    temp_url = ""
    link_to = linkTo
    msg_text = ""
    template = ""

    print("1---------------------------")

    if is_verification:
        temp_url = verify_url
        msg_text = "In Order To Verify Your Email Address"

        template = """
        <html xmlns=3D"http://www.w3.org/1999/xhtml" lang=3D"en" xml:lang=3D"en"><h=
        ead><meta http-equiv=3D"Content-Type" content=3D"text/html; charset=3Dutf-8=
        "><meta name=3D"viewport" content=3D"width=3Ddevice-width"><title>&#1071;&#=
        1082;&#1097;&#1086; &#1082;&#1091;&#1087;&#1091;&#1074;&#1072;&#1090;&#1080=
        ;, &#1090;&#1086; &#1085;&#1072;&#1081;&#1082;&#1088;&#1072;&#1097;&#1077;.=
         &#1055;&#1088;&#1086;&#1087;&#1086;&#1079;&#1080;&#1094;&#1110;&#1111;, &#=
        1087;&#1110;&#1076;&#1110;&#1073;&#1088;&#1072;&#1085;&#1110; &#1076;&#1083=
        ;&#1103; &#1074;&#1072;&#1089;</title><style>
        @media only screen
        {
        html
        {
        background: #E5E5E5;
        min-height: 100%;
        }
        }
        @media only screen and (max-width:666px)
        {
        .small-
        {
        float: none!important;
        margin: 0 auto!important;
        text-align: center!important;
        }
        }
        @media only screen and (max-width:666px){
        table.body table.container .show-for-large{
        display: none!important;
        mso-hide: all;
        overflow: hidden;
        width: 0;
        }
        table.body table.container .hide-for-large{
        display: inline-block!important;
        }
        }
        @media only screen and (max-width:666px)
        {
        table.body img
        {
        height: auto;
        width: auto;
        }
        table.body center
        {
        min-width: 0!important;
        }
        table.body .container
        {
        width: 100%!important;
        }
        table.body .columns
        {
        box-sizing: border-box;
        height: auto!important;
        moz-box-sizing: border-box;
        webkit-box-sizing: border-box;
        }
        .large-offset-1{
        padding-left: 0 !important;
        padding-right: 0 !important;
        }
        
        th.small-12
        {
        display: inline-block!important;
        width: 100%!important;
        }
        table.menu
        {
        width: 100%!important;
        }
        table.menu td,table.menu th
        {
        display: inline-block!important;
        width: auto!important;
        text-align: center;
        }
        table.menu[align=3Dcenter]
        {
        width: auto!important;
        }
        }
        @media only screen and (max-width:666px){
        .pad-bt {padding-bottom: 16px!important;}
        .pad-bt-sm {padding-bottom: 4px!important;}
        .pad-bt-none {padding-bottom: 0px!important;}
        .btn-more-link{font-size: 16px !important; line-height:40px !important; pad=
        ding: 0 16px !important;}
        .picture-wrap{height: auto !important;}
        .text-title{font-size: 21px !important;line-height: 24px!important; text-al=
        ign: left !important;}
        .text-description{font-size: 14px !important; text-align: left !important;}
        .subscribes{width: 100% !important;}
        .purchase-description{padding-left: 16px !important;}
        .goods-price{ width: auto !important;display: inline-block !important;}
        
        .goods-button_wrap {width: auto !important;display: table-cell !important;p=
        adding-top: 0 !important; text-align: right!important;}
        
        .goods-description{padding-left: 0 !important; padding-top: 16px !important=
        ;}
        .price-inner{width: 100% !important;}
        .picture-feedback{max-width:64px !important; max-height:64px !important;}
        .title-feedback{font-size: 17px !important;}
        .small-text-center{text-align: center!important;}
        .small-text-right{text-align: right!important;}
        .small-text-left{text-align: left!important;}
        .promocode {font-size: 20px!important;line-height: 36px!important;}
        .promocode-new{font-size: 18px!important;line-height: 20px!important;}
        .picture-look{width: 32px !important;}
        th.small-12.promotion{width: 288px !important;display: block!important;}
        th.price-block{display: table-cell !important;}
        
        .premium-column{display: inline-block !important; width:auto !important;tex=
        t-align: center !important;}
        .premium-description{padding-left: 16px !important;display: table-cell !imp=
        ortant;}
        .premium-logo{max-width: 56px !important; height: 56px;}
        .premium-logo-sm{max-width: 176px !important;height: 12px;}
        
        .premium-block span{display: block !important; text-align: center !importan=
        t;}
        .bonus-link{display: block !important; text-align: center !important;font-s=
        ize: 10px !important;line-height: 11px !important; padding-top: 4px;}
        
        
        .premium-old_price{font-size: 18px !important;line-height: 21px !important;=
        }
        .premium-old_price span{font-size: 14px !important;}
        .premium-new_price{font-size: 36px !important;line-height: 41px !important;=
        }
        .premium-new_price span{font-size: 24px !important;}
        
        .goods-title{font-size: 18px!important;line-height: 21px!important;}
        .goods-price_new{font-size: 24px!important;line-height: 28px!important;}
        .goods-price_old{font-size: 14px!important;line-height: 16px!important;}
        .goods-item{border-right: none!important; }
        .row-description{padding:0px 16px !important;}
        
        .goods-price-arrow{font-size: 22px!important;line-height: 22px!important;}
        .promotoin-block{padding: 0 8px !important; padding-top: 8px !important;}
        }
        </style></head><body style=3D"-moz-box-sizing:border-box;-ms-text-size-adju=
        st:100%;-webkit-box-sizing:border-box;-webkit-text-size-adjust:100%;Margin:=
        0;box-sizing:border-box;margin:0;min-width:100%;padding:0;text-align:left;w=
        idth:100%!important"><span style=3D"color: transparent; display: none !impo=
        rtant; font-size: 0px; line-height: 0px; height: 0; max-height: 0; max-widt=
        h: 0; opacity: 0; overflow: hidden; mso-hide: all; visibility: hidden; widt=
        h: 0;">&#1052;&#1086;&#1078;&#1085;&#1072; &#1086;&#1073;&#1088;&#1072;&#10=
        90;&#1080; &#1087;&#1086;&#1076;&#1072;&#1088;&#1091;&#1085;&#1086;&#1082; =
        &#1082;&#1086;&#1093;&#1072;&#1085;&#1080;&#1084; &#1110; &#1089;&#1086;&#1=
        073;&#1110;</span><div style=3D"display: none; max-height: 0px; overflow: h=
        idden;">&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&=
        zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwn=
        j;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&=
        nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbs=
        p;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&=
        zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwn=
        j;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&=
        nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbs=
        p;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&=
        zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwn=
        j;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&=
        nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbs=
        p;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&=
        zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwn=
        j;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&=
        nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbs=
        p;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&=
        zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwn=
        j;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&=
        nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbs=
        p;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&=
        zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwn=
        j;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&=
        nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbs=
        p;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&=
        zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwn=
        j;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&=
        nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbs=
        p;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&=
        zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwn=
        j;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&=
        nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbs=
        p;&zwnj;&nbsp;</div><img width=3D"1" height=3D"1" alt=3D"" src=3D"https://c=
        dn.rozetka.com.ua/rozetka/e/CgxaXzxt-YN6W7N_7cYSIGZXdtOE3fKLQM9dkB0Vau0b1Lp=
        YAaTCsjnqcmaAEMsIMc0B2DhA-thB.4nQArqd1-8BBdw/open">
        
        <table class=3D"body" style=3D"Margin:0;background:#E5E5E5;border-collapse:=
        collapse;color:#333;font-family:Arial, Helvetica, sans-serif;font-weight:40=
        0;height:100%;margin:0;padding:0;width:100%"><tr><td class=3D"center" align=
        =3D"center" valign=3D"top" style=3D"Margin:0;margin:0;padding:0;text-align:=
        left;vertical-align:middle;">
        <center data-parsed=3D"" style=3D"min-width:650px;width:100%">
        
        <!--container -->=20
        <table align=3D"center" class=3D"container" style=3D"Margin:0 auto;border-c=
        ollapse:collapse;margin:0 auto;padding:0;width:650px"><tr><td style=3D"Marg=
        in:0;margin:0;padding:0;">
        <table class=3D"row" style=3D"border-collapse:collapse;display:table;paddin=
        g:0;position:relative;width:100%"><!-- content--><tr><td style=3D"Margin:0;=
        margin:0;padding:0;">
        <table class=3D"container" style=3D"Margin:0 auto;background:#fff;font-fami=
        ly:Arial, Helvetica, sans-serif;border-collapse:collapse;margin:0;margin:0 =
        auto;padding:0;width:650px"><tr><td style=3D"Margin:0;margin:0; padding:0;"=
        >
        <table style=3D"border-collapse:collapse;display:table;padding:0;position:r=
        elative;width:100%"><!-- header--><tr><td style=3D"Margin:0;margin:0;paddin=
        g:0;">
        <table align=3D"center" class=3D"container" style=3D"Margin:0 auto;border-c=
        ollapse:collapse;margin:0;margin:0 auto;padding:0;width:650px;"><tr><td hei=
        ght=3D"16" style=3D"line-height:16px; height:16px; padding: 0;">&#160;</td>
        </tr><tr><td style=3D"Margin:0;margin:0; padding: 0 16px;">
        <table style=3D"border-collapse:collapse;display:table;padding:0;position:r=
        elative;width:100%"><tr><!--logo--><th style=3D"Margin:0 auto;margin:0 auto=
        ;padding:0;text-align: left;">
        <table style=3D"border-collapse:collapse;padding:0;width:100%;text-align: l=
        eft;"><tr><!-- logo large--><th class=3D"small-12 columns pad-bt show-for-l=
        arge" style=3D"Margin:0 auto;margin:0 auto;padding:0;width:237px; text-alig=
        n: center;display:inline-block;">
        <a href=3D"https://rozetka.com.ua/?iitt=3DVuU9RM4lhMPshF6d4IYj4Dnd4XTT&amp;=
        utm_source=3Ddm&amp;utm_campaign=3Dpersonal_promo&amp;utm_medium=3Demail&am=
        p;xnpe_cmp=3D.eJwTUkgLL7vccvdTt8P52Amyollvpa_simBccmiT5auitAaB0xyKZxlvWDj8u=
        uGoVaevn5SfUqlfkpiUk6pfUqRfkqKfnJpXklqEIgRjRxvGInPxSEUboanMACtA5SYCAGV0QYg.=
        TmDZ9fAS684TzrOb6VNgWYKB5k4" title=3D"ROZETKA" target=3D"_blank" style=3D"c=
        olor:#FF7878; font-family:Arial, Helvetica, sans-serif; font-size:14px;Marg=
        in:0;margin:0;padding:0;">
        <img src=3D"https://content.rozetka.com.ua/files/images/original/187945023.=
        png" width=3D"237" height=3D"40" border=3D"0" alt=3D"ROZETKA" data-pin-nopi=
        n=3D"true" style=3D"display:block;margin:0 auto;max-width:237px;width:auto;=
        "></a>
        </th>
        <!-- logo large-->
        
        
        <!-- logo small-->
        <th class=3D"columns hide-for-large" style=3D"Margin:0 auto;margin:0 auto;p=
        adding:0;text-align: center; display: none;overflow: hidden;">
        <a href=3D"https://rozetka.com.ua/?iitt=3DVuU9RM4lhMPshF6d4IYj4Dnd4XTT&amp;=
        utm_source=3Ddm&amp;utm_campaign=3Dpersonal_promo&amp;utm_medium=3Demail&am=
        p;xnpe_cmp=3D.eJwTUkgLL7vccvdTt8P52Amyollvpa_simBccmiT5auitAaB0xyKZxlvWDj8u=
        uGoVaevn5SfUqlfkpiUk6pfUqRfkqKfnJpXklqEIgRjRxvGInPxSEUboanMACtA4gIVJAIAZXhB=
        iQ.9GTgqNElU3TIvmZROEnYkzZWIUg" title=3D"ROZETKA" target=3D"_blank" style=
        =3D"color:#FF7878; font-family:Arial, Helvetica, sans-serif; font-size:14px=
        ;Margin:0;margin:0;padding:0;">
        <img src=3D"https://content2.rozetka.com.ua/files/images/original/187945028=
        .png" width=3D"40" height=3D"40" border=3D"0" alt=3D"ROZETKA" data-pin-nopi=
        n=3D"true" style=3D"display:block;margin:0 auto;max-width:40px;width:auto;"=
        ></a>
        </th>
        <!-- logo small-->
        
        </tr></table></th>
        <!--logo-->
        
        <!--apps-->
        <!-- apps -->
        <th class=3D"columns" style=3D"Margin:0 auto;margin:0 auto;padding:0;paddin=
        g-left:24px;text-align: right;">
        <table style=3D"border-collapse:collapse;padding:0;width:100%;text-align: r=
        ight;"><tr><!-- apps large--><th class=3D"columns" style=3D"Margin:0 auto;m=
        argin:0 auto;padding:0;text-align:right;display: inline-block;height: 40px;=
        line-height: 40px;">
        <a href=3D"https://cdn.rozetka.com.ua/rozetka/e/.eJwTUkgLL7vccvdTt8P52Amyol=
        lvpa_simBccmiT5auitAaB0xxSUhklJQVW-vr5eak5mXnZeiX5-kX5Vakl2Yn6SsJFqemZxSWpR=
        akpVmamhubmJmbmhmcZb1g4_LrhaMXBxVRaLMSUkmslAmQlC_EVpBYV5-cl5sQXFOXn5ltxA0Vz=
        hVhTcxMzc6Kq9fWT8lMq9UsSk3JS9UuK9EtS9JNT84BmowjB2NGGschcPFLRRmgqM8AiCK5-IgC=
        fCF2_.LBrBRpwwGV6SiA/click" title=3D"APPS" target=3D"_blank" style=3D"color=
        :#FF7878; font-family:Arial, Helvetica, sans-serif; font-size:14px;Margin:0=
        ;margin:0;padding:0;">
        <img src=3D"https://content2.rozetka.com.ua/files/images/original/243313191=
        .png" width=3D"135" height=3D"40" border=3D"0" alt=3D"APPS" data-pin-nopin=
        =3D"true" style=3D"display:block;margin:0 auto;max-width:135px;width:auto;"=
        ></a>
        </th>
        <!-- apps large-->
        
        
        </tr></table></th>
        <!-- apps -->
        <!--apps-->
        
        </tr></table></td>
        </tr><tr><td height=3D"16" style=3D"line-height:16px; height:16px; padding:=
         0;">&#160;</td>
        </tr></table></td>
        </tr><!-- header--><!-- image--><tr><td style=3D"Margin:0;margin:0;padding:=
        0;">
        <table align=3D"center" class=3D"container" style=3D"Margin:0 auto;border-c=
        ollapse:collapse;margin:0 auto;padding:0;width:650px;"><tr><td style=3D"Mar=
        gin:0;margin:0; padding:0;">
        <table class=3D"row" style=3D"border-collapse:collapse;display:table;paddin=
        g:0;position:relative;width:100%;"><tr><td style=3D"Margin:0;margin:0;paddi=
        ng:0;">
        <a href=3D"https://rozetka.com.ua/ua/promo/lovesale/?iitt=3DVuU9RM4lhMPshF6=
        d4IYj4Dnd4XTT&amp;utm_source=3Ddm&amp;utm_campaign=3Dpersonal_promo&amp;utm=
        _medium=3Demail&amp;xnpe_cmp=3D.eJwTUkgLL7vccvdTt8P52Amyollvpa_simBccmiT5au=
        itAaB0xyKZxlvWDj8uuGolamvn5SfUqlfkpiUk6pfUqRfkqKfnJpXklqEIgRjRxvGInNRpIxwSo=
        HYiQBE2zpd.UgW2Ebk8PVeHijCz30Oq-deTkAo" target=3D"_blank" style=3D"Margin:0=
        ;color:#221F1F!important;font-size:24px;margin:0;padding:0;"><img src=3D"ht=
        tps://content.rozetka.com.ua/files/images/original/311144251.jpg" alt=3D"&#=
        1056;&#1077;&#1082;&#1086;&#1084;&#1077;&#1085;&#1076;&#1091;&#1108;&#1084;=
        &#1086; &#1082;&#1091;&#1087;&#1080;&#1090;&#1080; &#1085;&#1072; &#1088;&#=
        1086;&#1079;&#1087;&#1088;&#1086;&#1076;&#1072;&#1078;&#1110;" border=3D"0"=
         style=3D"display:block;margin:0 auto;max-width:100%;width:auto;"></a>
        </td>
        </tr></table></td>
        </tr></table></td>
        </tr><!-- image--><!-- 1 GOODS ROW--><tr><td style=3D"Margin:0;margin:0;pad=
        ding:0 16px;">
        <table style=3D"border-collapse:collapse;display:table;padding:0;position:r=
        elative;width:100%;"><tr><!-- goods item --><th class=3D"small-12 columns g=
        oods-block" style=3D"Margin:0 auto;margin:0 auto;padding:0;padding-bottom:1=
        6px; padding-top:16px;border-bottom:#eaeaea 1px solid;vertical-align: top;"=
        >
        <table style=3D"border-collapse:collapse;display:table;padding:0;position:r=
        elative;width:100%;"><tr><th class=3D"small-12 columns" style=3D"Margin:0 a=
        uto;margin:0 auto;padding:0;width: 200px;vertical-align: middle;">
        <table style=3D"border-collapse:collapse;padding:0;width:100%"><tr><td clas=
        s=3D"picture-wrap" style=3D"Margin:0;margin:0; padding:0; height: 200px;">
        <a href=3D"https://rozetka.com.ua/apple_ipad_10_2_2021_wi_fi_64gb_silver/p3=
        18463099/?iitt=3DVuU9RM4lhMPshF6d4IYj4Dnd4XTT&amp;utm_source=3Ddm&amp;utm_c=
        ampaign=3Dpersonal_promo&amp;utm_medium=3Demail&amp;xnpe_cmp=3D.eJwTUkgLL7v=
        ccvdTt8P52Amyollvpa_simBccmiT5auitAaB0xyKZxlvWDj8uuGoVaGvn5SfUqlfkpiUk6pfUq=
        RfkqKfnJpXklqEIgRjRxvGInNRpIzRpDKQ2WCNSLoSAeLSP7E.qeTV87WrZnMt3MStNe3Cw4ekG=
        Kg">
        <img src=3D"https://content.rozetka.com.ua/goods/images/original/224010066.=
        jpg" border=3D"0" height=3D"184" style=3D"max-width:200px;width:auto;max-he=
        ight: 184px;height:auto;display:block; margin:0 auto;"></a>=20
        </td>
        </tr><!--legal image --><!--legal image --></table></th>
        
        
        
        <th class=3D"small-12 goods-description columns" style=3D"Margin:0 auto;mar=
        gin:0 auto;padding:0;vertical-align: top; padding-left: 16px;">
        <table style=3D"border-collapse:collapse;padding:0;width:100%"><tr><td styl=
        e=3D"Margin:0;margin:0; padding:0;line-height:20px;text-align:left;">
        <span style=3D"display:block;width:100%;">
        <a href=3D"https://rozetka.com.ua/apple_ipad_10_2_2021_wi_fi_64gb_silver/p3=
        18463099/?iitt=3DVuU9RM4lhMPshF6d4IYj4Dnd4XTT&amp;utm_source=3Ddm&amp;utm_c=
        ampaign=3Dpersonal_promo&amp;utm_medium=3Demail&amp;xnpe_cmp=3D.eJwTUkgLL7v=
        ccvdTt8P52Amyollvpa_simBccmiT5auitAaB0xyKZxlvWDj8uuGo1cCor5-Un1KpX5KYlJOqX1=
        KkX5Kin5yaV5JahCIEY0cbxiJzUaSM0aQykNnRRrHohhQXJObpJwIABoZChQ.83wu6rcPyw4aPy=
        eWXTXeBx-qUaQ" class=3D"goods-title" style=3D"Margin:0;color:#3e77aa;margin=
        :0;padding:0;text-decoration:none;font-weight: 400;font-size: 21px;line-hei=
        ght:24px;font-family:Arial, Helvetica, sans-serif;">&#1055;&#1083;&#1072;&#=
        1085;&#1096;&#1077;&#1090; Apple iPad 10.2" 2021 Wi-Fi 64 GB Silver (MK2L3R=
        K/A)</a></span>
        </td>
        </tr><tr><td height=3D"8" style=3D"line-height:8px; height:8px; padding: 0;=
        ">&#160;</td>
        </tr><tr><td style=3D"Margin:0;margin:0; padding:0;text-align:left;">
        <span style=3D"display:block;font-size:12px;width:100%;font-weight: 400; fo=
        nt-family:Arial, Helvetica, sans-serif;color: #221F1F;">&#1042;&#1072;&#109=
        6;&#1072; &#1077;&#1082;&#1086;&#1085;&#1086;&#1084;&#1110;&#1103;: <span s=
        tyle=3D"color:#F84147;">2000&#160;&#8372;</span></span></td>
        </tr><tr><td height=3D"16" style=3D"line-height:16px; height:16px; padding:=
         0;">&#160;</td>
        </tr><tr><th class=3D"small-12 columns" style=3D"Margin:0 auto;margin:0 aut=
        o;padding:0;">
        <table style=3D"border-collapse:collapse;padding:0;width:100%"><tr><!-- goo=
        ds prices --><td style=3D"Margin:0;margin:0; padding:0;text-align:left; ver=
        tical-align:middle;">
        <table style=3D"border-collapse:collapse;display:table;padding:0;position:r=
        elative;width:100%"><!-- old price --><tr><th style=3D"Margin:0;margin:0;pa=
        dding:0;text-align: left;">
        <span class=3D"goods-price_old" style=3D"color:#A6A5A5; font-size:18px; lin=
        e-height:21px; text-decoration:line-through; padding:0;text-decoration-colo=
        r: #A6A5A5; font-weight: 400;font-family:Arial, Helvetica, sans-serif;">169=
        99</span><span style=3D"font-size:12px;font-weight: 400;color:#A6A5A5;">&#1=
        60;&#8372;</span></th>
        </tr><!-- old price --><!-- new price --><tr><th style=3D"Margin:0;margin:0=
        ;padding:0;text-align: left;">
        <span class=3D"goods-price_new" style=3D"display:inline-block; text-align:c=
        enter; padding:0;color: #F84147; font-size:36px; line-height:41px;font-weig=
        ht: 400;font-family:Arial, Helvetica, sans-serif;">14999<span style=3D"font=
        -size:18px;">&#160;&#8372;</span></span>
        </th>
        </tr><!-- new price --></table></td>
        <!-- goods prices -->
        
        
        
        <!-- button_buy -->
        <td style=3D"Margin:0;margin:0; padding:0;text-align:right;vertical-align:b=
        ottom;">
        <table style=3D"border-collapse:collapse;display:table;padding:0;position:r=
        elative;width:100%"><tr><th style=3D"Margin:0;margin:0;padding:0;text-align=
        : right;">
        <span class=3D"btn-more" style=3D"text-align: center;vertical-align: middle=
        ;-webkit-border-radius: 4px;-moz-border-radius: 4px; border-radius: 4px; ba=
        ckground-color:#00A046;display: inline-block;">
        <a href=3D"https://rozetka.com.ua/apple_ipad_10_2_2021_wi_fi_64gb_silver/p3=
        18463099/?iitt=3DVuU9RM4lhMPshF6d4IYj4Dnd4XTT&amp;utm_source=3Ddm&amp;utm_c=
        ampaign=3Dpersonal_promo&amp;utm_medium=3Demail&amp;xnpe_cmp=3D.eJwTUkgLL7v=
        ccvdTt8P52Amyollvpa_simBccmiT5auitAaB0xyKZxlvWDj8uuGoNZtRXz8pP6VSvyQxKSdVv6=
        RIvyRFPzk1ryS1CEUIxo42jEXmokgZo0llILOjjWIRKk1jUWVTkGVBUsUFiXn6iQCilUw8.L-89=
        9BA8WT-9auYH7OHPXoujJbE" class=3D"btn-more-link-sm" style=3D"color: #fff;fo=
        nt-size:14px;font-weight:400;text-decoration: none;line-height:32px; displa=
        y: inline-block;padding: 0 16px;font-family:Arial, Helvetica, sans-serif;" =
        target=3D"_blank">&#1050;&#1091;&#1087;&#1080;&#1090;&#1080;</a>
        </span>
        </th>
        </tr></table></td>
        <!-- button_buy -->
        </tr></table></th>
        </tr></table></th>
        
        
        
        </tr></table></th>
        <!-- goods item -->
        
        
        </tr></table></td>
        </tr><!--1  GOODS ROW--><tr><td height=3D"32" style=3D"line-height:32px; he=
        ight:32px; padding: 0;">&#160;</td>
        </tr><!-- button--><tr><td style=3D"Margin:0;margin:0; padding:0;">
        <table class=3D"row" style=3D"border-collapse:collapse;display:table;paddin=
        g:0;position:relative;width:100%;text-align:center;"><tr><th style=3D"Margi=
        n:0;margin:0;padding:0;">
        <center data-parsed=3D"" style=3D"width:100%;">=20
        <span class=3D"btn-more" style=3D"text-align: center;vertical-align: middle=
        ;-webkit-border-radius: 4px;-moz-border-radius: 4px; border-radius: 4px; ba=
        ckground-color: #00A046;display: inline-block;">
        <a href=3D"https://rozetka.com.ua/ua/promo/lovesale/?iitt=3DVuU9RM4lhMPshF6=
        d4IYj4Dnd4XTT&amp;utm_source=3Ddm&amp;utm_campaign=3Dpersonal_promo&amp;utm=
        _medium=3Demail&amp;xnpe_cmp=3D.eJwTUkgLL7vccvdTt8P52Amyollvpa_simBccmiT5au=
        itAaB0xyKZxlvWDj8uuGolamvn5SfUqlfkpiUk6pfUqRfkqKfnJpXklqEIgRjRxvGInNRpEzRpD=
        JgBhUXJObpJwIARu06og.xsTH04a-MUiUgQW75gWCx2gJq_s" class=3D"btn-more-link" s=
        tyle=3D"color: #fff;font-size:18px;font-weight:400;text-decoration: none;li=
        ne-height:48px; display: inline-block;padding: 0 24px;font-family:Arial, He=
        lvetica, sans-serif;" target=3D"_blank">&#1041;&#1110;&#1083;&#1100;&#1096;=
        &#1077; &#1090;&#1086;&#1074;&#1072;&#1088;&#1110;&#1074; &#1088;&#1086;&#1=
        079;&#1087;&#1088;&#1086;&#1076;&#1072;&#1078;&#1091;</a>
        </span>
        </center>
        </th>
        
        </tr></table></td>
        </tr><!-- button--><tr><td height=3D"48" style=3D"line-height:48px; height:=
        48px; padding:0;">&#160;</td>
        </tr></table></td>
        </tr></table></td>
        </tr><!-- content--><!-- footer--><tr><td style=3D"Margin:0;margin:0;paddin=
        g:0;">
        <table align=3D"center" class=3D"container" style=3D"Margin:0 auto;backgrou=
        nd:#f7f7f7;border-top: #eaeaea 1px solid;border-collapse:collapse;margin:0 =
        auto;padding:0;width:650px;"><tr><td style=3D"Margin:0;margin:0; padding:0;=
        ">
        <table style=3D"border-collapse:collapse;display:table;padding:0;position:r=
        elative;width:100%"><!-- image--><tr><td style=3D"Margin:0;margin:0;padding=
        :0;">=20
        <table align=3D"center" class=3D"container" style=3D"Margin:0 auto;border-c=
        ollapse:collapse;margin:0 auto;padding:0;width:650px;"><tr><td style=3D"Mar=
        gin:0;margin:0; padding:0;">=20
        <table class=3D"row" style=3D"border-collapse:collapse;display:table;paddin=
        g:0;position:relative;width:100%;"><tr><td style=3D"Margin:0;margin:0;paddi=
        ng:0;">=20
        <a href=3D"https://rozetka.com.ua/ua/pages/open_points/?iitt=3DVuU9RM4lhMPs=
        hF6d4IYj4Dnd4XTT&amp;utm_source=3Ddm&amp;utm_campaign=3Dpersonal_promo&amp;=
        utm_medium=3Demail&amp;xnpe_cmp=3D.eJwTUkgLL7vccvdTt8P52Amyollvpa_simBccmiT=
        5auitAaB0xyKZxlvWDj8uuGolamvn5SfUqlfkpiUk6pfUqRfkqKfnJpXklqEIgRjRxvFInNRpAx=
        xSoHYiQBE9jpd.HQvQ303N1FTs1ZE_Jrj8pLUo0Yo" target=3D"_blank" style=3D"Margi=
        n:0;color:#FFF!important;font-size:24px;;margin:0;padding:0;"><img src=3D"h=
        ttps://content2.rozetka.com.ua/files/images/original/310407657.jpg" border=
        =3D"0" style=3D"display:block;margin:0 auto;max-width:100%;width:auto;"></a=
        >=20
        </td>=20
        </tr></table></td>=20
        </tr></table></td>=20
        </tr><!-- image--><!-- social --><!-- survey --><tr><td style=3D"Margin:0;m=
        argin:0; padding:0; padding:16px 16px;text-align: center; background-color:=
        #f7f7f7;border-bottom: #eaeaea 1px solid;">
        <table class=3D"row" style=3D"border-collapse:collapse;display:table;paddin=
        g:0;position:relative;width:100%;text-align: center;"><tr></tr><tr><td styl=
        e=3D"Margin:0;margin:0; padding:0; display: inline-block; text-align: cente=
        r;">
        <table class=3D"row" style=3D"border-collapse:collapse;display:table;paddin=
        g:0;position:relative;width:100%;text-align: center;"><tr><th class=3D"smal=
        l-12 columns" style=3D"Margin:0 auto;margin:0 auto;padding:0;text-align: ce=
        nter;vertical-align: middle;">
        <span style=3D"Margin:0;color: #000;margin:0;font-weight: 400;font-size: 14=
        px;line-height: 16px;font-family:Arial, Helvetica, sans-serif;">&#1062;&#10=
        77;&#1081; &#1083;&#1080;&#1089;&#1090; &#1073;&#1091;&#1074; &#1076;&#1083=
        ;&#1103; &#1074;&#1072;&#1089; &#1082;&#1086;&#1088;&#1080;&#1089;&#1085;&#=
        1080;&#1084;?</span>
        </th>
        
        
        
        <th class=3D"small-12 columns goods-description" style=3D"Margin:0 auto;mar=
        gin:0 auto;padding:0;padding-left: 16px;">
        <table class=3D"menu" style=3D"border-collapse:collapse;padding:0;width:100=
        %;text-align: center;"><tr><td style=3D"Margin:0;margin:0; padding:0;text-a=
        lign:right;vertical-align:middle;">
        <table style=3D"border-collapse:collapse;display:table;padding:0;position:r=
        elative;width:100%"><tr><!-- btn --><td style=3D"Margin:0;margin:0;padding:=
        0; padding-right: 16px;">
        <span style=3D"text-align: center;vertical-align: middle;-webkit-border-rad=
        ius: 4px;-moz-border-radius: 4px; border-radius: 4px; border: #eaeaea 1px s=
        olid;display: inline-block;">
        <a href=3D"https://cdn.rozetka.com.ua/rozetka/e/.eJwTUkgLL7vccvdTt8P52Amyol=
        lvpa_simBccmiT5auitAaB0xxSexkzSkoKiq309ZNT8vSK8qtSS7IT9ZLzc_VKE_WhXP1i_dRKr=
        6yUCD-DJCPDnOQcy4IoZ08zz6ywDL_wyKrIqqjsqKxsE9-qFCDfKxNI50aFB2X5ZXoWe-b5GSbn=
        ReWkhsH0RFb4h_tl-4dEGviG-GVG5gbl-mZlV0bl-mX7GgVWRmV6WeoVG-QGlYab-1haZhXruoa=
        HmAa5lZWZuWWEVRTbl5bkxifn55Wk5pXYVqYWKwkXpaZnFpekFqWmWJmZGpqbm5iZG55lvGHh8O=
        uGoxUHF1NpsRBTSq6VCJCVLMRXkFpUnJ-XmBNfUJSfm2_FDRTNFWJNzU3MzInqZ9TXT8pPqdQvS=
        UzKSdUvKdIvSdFPBlqUWoQiBGNHG8Uic_FIYajMAItg0QhkRxvG6hcXJObpJwIA0h6e3A.-OWnf=
        axH3dVKag/click" style=3D"color: #000;text-decoration: none;line-height:40p=
        x;height: 40px; display: inline-block;padding: 0 16px;font-family:Arial, He=
        lvetica, sans-serif;vertical-align: middle;" target=3D"_blank">
        <span style=3D"Margin:0;font-size:14px;line-height:16px;font-weight:400;mar=
        gin:0;padding:0;font-family:Arial,Helvetica,sans-serif; vertical-align: mid=
        dle;">&#1058;&#1072;&#1082;</span>
        <span style=3D"Margin:0; padding-left: 8px;"><img src=3D"https://content.ro=
        zetka.com.ua/files/images/original/238340473.png" width=3D"22" height=3D"22=
        " border=3D"0" style=3D"border:none;margin:0 auto;max-width:22px;vertical-a=
        lign: middle;"></span>
        </a>
        </span>
        </td>
        <!-- btn -->
        
        <!-- btn -->
        <td style=3D"Margin:0;margin:0;padding:0;">
        <span style=3D"text-align: center;vertical-align: middle;-webkit-border-rad=
        ius: 4px;-moz-border-radius: 4px; border-radius: 4px; border: #eaeaea 1px s=
        olid;display: inline-block;">
        <a href=3D"https://cdn.rozetka.com.ua/rozetka/e/.eJwTUkgLL7vccvdTt8P52Amyol=
        lvpa_simBccmiT5auitAaB0xxSexgzSkoKiq309ZNT8vSK8qtSS7IT9ZLzc_VKE_WhXP1i_dRKr=
        6yUCD-DJCPDnOQcy4IoZ08zz6ywDL_wyKrIqqjsqKxsE9-qFCDfKxNI50aFB2X5ZXoWe-b5GSbn=
        ReWkhsH0RFb4h_tl-4e45fqG-GVG5gbl-mZlV0bl-mX7GgVWRgZ7WerlFhT7F2TkB5eFJuVlFuq=
        GFJl7mhvkeBRlOrval5bkxifn55Wk5pXY5uUrCRelpmcWl6QWpaZYmZkampubmJkbnmW8YeHw64=
        ajFQcXU2mxEFNKrpUIkJUsxFeQWlScn5eYE19QlJ-bb8UNFM0VYk3NTczMiepn1NdPyk-p1C9JT=
        MpJ1S8p0i9J0U8G2pNahCIEY0cbxSJz8UhhqMwAi2DRCGSDpIoLEvP0EwHbnp8f.oi8gFZLkCdh=
        qFA/click" style=3D"color: #000;text-decoration: none;line-height:40px;heig=
        ht: 40px; display: inline-block;padding: 0 16px;font-family:Arial, Helvetic=
        a, sans-serif;vertical-align: middle;" target=3D"_blank">
        <span style=3D"Margin:0;font-size:14px;line-height:16px;font-weight:400;mar=
        gin:0;padding:0;font-family:Arial,Helvetica,sans-serif; vertical-align: mid=
        dle;">&#1053;&#1110;</span>
        <span style=3D"Margin:0;  padding-left: 8px;"><img src=3D"https://content.r=
        ozetka.com.ua/files/images/original/238340474.png" width=3D"22" height=3D"2=
        2" border=3D"0" style=3D"border:none;margin:0 auto;max-width:22px;vertical-=
        align: middle;"></span>
        </a>
        </span>
        </td>
        <!-- btn -->
        
        
        </tr></table></td>
        </tr></table></th>
        
        
        
        
        </tr></table></td>
        </tr></table></td>
        </tr><!-- survey --><!-- social --><tr><td style=3D"Margin:0;margin:0; padd=
        ing:16px 16px;">
        <table class=3D"row" style=3D"border-collapse:collapse;display:table;paddin=
        g:0;position:relative;width:100%;"><tr><th class=3D"small-12 columns pad-bt=
        " style=3D"Margin:0 auto;margin:0 auto;padding:0;width:212px">
        <table class=3D"menu" style=3D"border-collapse:collapse;padding:0;width:100=
        %;text-align: center;"><tr><th title=3D"App Store" style=3D"Margin:0 auto;m=
        argin:0 auto;padding:0;padding-right:8px;">
        <a href=3D"https://cdn.rozetka.com.ua/rozetka/e/.eJwTUkgLL7vccvdTt8P52Amyol=
        lvpa_simBccmiT5auitAaB0xxSxhklJQXFVvr6mSWleanFeokFBTmpesn5ufqlxfpAjn5RflVqS=
        XaifmaKuYmBiZmlmbGhknBRanpmcUlqUWqKlZmpobm5iZm54VnGGxYOv244WnFwMZUWCzGl5FqJ=
        AFnJQnwFqUXF-XmJOfEFRfm5-VbcQNFcIdbU3MTMnKh8ff2k_JRK_ZLEpJxU_ZIi_ZIU_eTUPKD=
        ZKEIwdrRRLDIXRcoYTSoj2jAWnZsIAC0OYV0.1H3bUiz5O76liw/click" target=3D"_blank=
        " style=3D"Margin:0;color:#FF7878;font-weight:400;margin:0;padding:0;text-a=
        lign:left;text-decoration:none">=20
        <img src=3D"https://content1.rozetka.com.ua/files/images/original/193138795=
        .png" alt=3D"App Store" width=3D"102" height=3D"32" border=3D"0" style=3D"b=
        order:none;display:block;margin:0 auto;max-width:102px;"></a>
        </th>
        
        <th title=3D"Google Play" style=3D"Margin:0 auto;margin:0 auto;padding:0;">
        <a href=3D"https://cdn.rozetka.com.ua/rozetka/e/.eJwTUkgLL7vccvdTt8P52Amyol=
        lvpa_simBccmiT5auitAaB0xxSjhklJQXFVvr6BTmJlXrp-fnpOal6yfm5-sUl-UWp-okFBcX6K=
        akliZk5xfaZKbaliSBJvaL8qtSS7ES94oz8AiXhotT0zOKS1KLUFCszU0NzcxMzc8OzjDcsHH7d=
        cLTi4GIqLRZiSsm1EgGykoX4ClKLivPzEnPiC4ryc_OtuIGiuUKsqblAK6Ly9fWT8lMq9UsSk3J=
        S9UuK9EtS9JNT84BmowjB2NFGschcFCljNKmMaMNYFC5QbyIAdo1oYQ.1fjNivBaoxttdQ/clic=
        k" target=3D"_blank" style=3D"Margin:0;color:#FF7878;font-weight:400;margin=
        :0;padding:0;text-align:left;text-decoration:none">
        <img src=3D"https://content1.rozetka.com.ua/files/images/original/193138797=
        .png" alt=3D"Google play" width=3D"102" height=3D"32" border=3D"0" style=3D=
        "border:none;display:block;margin:0 auto;max-width:102px;"></a>
        </th>
        
        
        </tr></table></th>
        
        
        
        
        
        
        
        <th class=3D"small-12 columns large-offset-1" style=3D"Margin:0 auto;margin=
        :0 auto;padding:0;width:184px;padding-left:200px;">
        <table class=3D"menu" style=3D"border-collapse:collapse;padding:0;width:100=
        %;text-align: center;"><tr><th title=3D"Facebook" style=3D"width:24px;verti=
        cal-align:middle;padding-left:0px;">
        <a href=3D"https://cdn.rozetka.com.ua/rozetka/e/.eJwTUkgLL7vccvdTt8P52Amyol=
        lvpa_simBccmiT5auitAaB0xxSyhklJQXFVvr65eXlemmJyalJ-fnZesn5ufpF-VWpJdmJeqWJS=
        sJFqemZxSWpRakpVmamhubmJmbmhmcZb1g4_LrhaMXBxVRaLMSUkmslAmQlC_EVpBYV5-cl5sQX=
        FOXn5ltxA0VzhVhTcxMzc6Ly9fWT8lMq9UsSk3JS9UuK9EtS9JNT84BmowjB2NFGschcFCljNKk=
        MsGIkrmGsfiIA47Bc7A.SyBOdTdjBVoI5g/click" target=3D"_blank" style=3D"Margin=
        :0;color:#FF7878;font-weight:400;margin:0;padding:0;text-align:left;text-de=
        coration:none">
        <img src=3D"https://content1.rozetka.com.ua/files/images/original/193097859=
        .png" width=3D"24" height=3D"24" border=3D"0" style=3D"border:none;display:=
        block;margin:0 auto;max-width:24px;"></a>
        </th>
        
        
        <th title=3D"Twitter" style=3D"width:24px;vertical-align:middle;padding-lef=
        t:8px;">
        <a href=3D"https://cdn.rozetka.com.ua/rozetka/e/.eJwTUkgLL7vccvdTt8P52Amyol=
        lvpa_simBccmiT5auitAaB0xxSchklJQXFVvr6JeWZJSWpRXrJ-bn6RflVqSXZifGliUrCRanpm=
        cVAidQUKzNTQ3NzEzNzw7OMNywcft1wtOLgYiotFmJKybUSAbKShfgKUouK8_MSc-ILivJz8624=
        gaK5QqypuYmZOVH5-vpJ-SmV-iWJSTmp-iVF-iUp-smpeUCzUYRg7GijWGQuipQxmlQGWDEqNxE=
        AMxlbXw.NlcwDGye9RWABQ/click" target=3D"_blank" style=3D"Margin:0;color:#FF=
        7878;font-weight:400;margin:0;padding:0;text-align:left;text-decoration:non=
        e">
        <img src=3D"https://content2.rozetka.com.ua/files/images/original/193097871=
        .png" width=3D"24" height=3D"24" border=3D"0" style=3D"border:none;display:=
        block;margin:0 auto;max-width:24px;"></a>
        </th>
        
        
        <th title=3D"YouTube" style=3D"width:24px;vertical-align:middle;padding-lef=
        t:8px;">
        <a href=3D"https://cdn.rozetka.com.ua/rozetka/e/.eJwTUkgLL7vccvdTt8P52Amyol=
        lvpa_simBccmiT5auitAaB0xxS3hklJQXFVvr65eXlepX5pSWlSal6yfm5-skZiXl5qTn6oc5F5=
        kWGulXmliGRaYXBRp4BqUFBJuaO9sWlSfHJ-XlpmUW5iSWZ-Xm2hkrCRanpmcUlqUWpKVZmpobm=
        5iZm5oZnGW9YOPy64WjFwcVUWizElJJrJQJkJQvxFaQWFefnJebEFxTl5-ZbcQNFc4VYU3MTM3O=
        i8vX1k_JTKvVLEpNyUvVLivRLUvSTU_OAZqMIwdjRRrHIXBQpYzSpDLBiJC5QQSIAoZBqng.fFY=
        PMb2-Hp-BUw/click" target=3D"_blank" style=3D"Margin:0;color:#FF7878;font-w=
        eight:400;margin:0;padding:0;text-align:left;text-decoration:none">
        <img src=3D"https://content1.rozetka.com.ua/files/images/original/193097880=
        .png" width=3D"24" height=3D"24" border=3D"0" style=3D"border:none;display:=
        block;margin:0 auto;max-width:24px;"></a>
        </th>
        
        <th title=3D"Instagram" style=3D"width:24px;vertical-align:middle;padding-l=
        eft:8px;">
        <a href=3D"https://cdn.rozetka.com.ua/rozetka/e/.eJwTUkgLL7vccvdTt8P52Amyol=
        lvpa_simBccmiT5auitAaB0xxSChklJQXFVvr6mXnFJYnpRYm5esn5ufpF-VWpJdmJpYn6SsJFq=
        emZxSWpRakpVmamhubmJmbmhmcZb1g4_LrhaMXBxVRaLMSUkmslAmQlC_EVpBYV5-cl5sQXFOXn=
        5ltxA0VzhVhTcxMzc6Ly9fWT8lMq9UsSk3JS9UuK9EtS9JNT84BmowjB2NFGschcFCljNKkMsGI=
        krkmsfiIAzDtb5g.VxWXAQqKynXyCg/click" target=3D"_blank" style=3D"Margin:0;c=
        olor:#FF7878;font-weight:400;margin:0;padding:0;text-align:left;text-decora=
        tion:none">
        <img src=3D"https://content.rozetka.com.ua/files/images/original/193097863.=
        png" width=3D"24" height=3D"24" border=3D"0" style=3D"border:none;display:b=
        lock;margin:0 auto;max-width:24px;"></a>
        </th>
        
        <th title=3D"Viber" style=3D"width:24px;vertical-align:middle;padding-left:=
        8px;">
        <a href=3D"https://cdn.rozetka.com.ua/rozetka/e/.eJwTUkgLL7vccvdTt8P52Amyol=
        lvpa_simBccmiT5auitAaB0xxSmRklJQXFVvr6mXllmSWpemWZSalFesn5ufr26Ua2joFOlrnlv=
        qpGbqZpQKLCKzTHtyLAJMwyLafISNXIqSwixNnQt6Aixd0tyiDALAWoptgsvBhIuaUCicASn8yo=
        ckcTVyOL4iwl4aLU9MziktSi1BQrM1NDc3MTM3PDs4w3LBx-3XC04uBiKi0WYkrJtRIBspKF-Ap=
        Si4rz8xJz4guK8nPzrbiBorlCrKm5iZk5Ufn6-kn5KZX6JYlJOan6JUX6JSn6yal5QLNRhGDsaK=
        NYZC6KlDGaVAZYMRLXNFY_EQCVEHE9.XG-DDKrKvEiqzg/click" target=3D"_blank" styl=
        e=3D"Margin:0;color:#FF7878;font-weight:400;margin:0;padding:0;text-align:l=
        eft;text-decoration:none">
        <img src=3D"https://content2.rozetka.com.ua/files/images/original/193097873=
        .png" width=3D"24" height=3D"24" border=3D"0" style=3D"border:none;display:=
        block;margin:0 auto;max-width:24px;"></a>
        </th>
        
        <th title=3D"Telegram" style=3D"width:24px;vertical-align:middle;padding-le=
        ft:8px;">
        <a href=3D"https://cdn.rozetka.com.ua/rozetka/e/.eJwTUkgLL7vccvdTt8P52Amyol=
        lvpa_simBccmiT5auitAaB0xxSohklJQXFVvr6JXq5qfpFRflVqSXZiUrCRanpmcUlqUWpKVZmp=
        obm5iZm5oZnGW9YOPy64WjFwcVUWizElJJrJQJkJQvxFaQWFefnJebEFxTl5-ZbcQNFc4VYU3MT=
        M3Oi8vX1k_JTKvVLEpNyUvVLivRLUvSTU_OAZqMIwdjRRrHIXBQpYzSpDLBiJK5ZrH4iAG7MV4s=
        .C0biyZdnwfXAtA/click" target=3D"_blank" style=3D"Margin:0;color:#FF7878;fo=
        nt-weight:400;margin:0;padding:0;text-align:left;text-decoration:none">
        <img src=3D"https://content1.rozetka.com.ua/files/images/original/193097870=
        .png" width=3D"24" height=3D"24" border=3D"0" style=3D"border:none;display:=
        block;margin:0 auto;max-width:24px;"></a>
        </th>
        
        
        </tr></table></th>
        
        
        
        </tr></table></td>
        </tr><!-- social end--><!-- social end--><!-- contact--><tr><td style=3D"Ma=
        rgin:0;margin:0; padding:16px 16px;border-top:#eaeaea 1px solid;">
        <table class=3D"row" style=3D"border-collapse:collapse;display:table;paddin=
        g:0;position:relative;width:100%;"><tr><!-- contact shop--><th class=3D"sma=
        ll-12 columns pad-bt small-text-center" style=3D"Margin:0 auto;margin:0 aut=
        o;padding:0;width:309px;vertical-align: top;text-align: center;"><span styl=
        e=3D"Margin:0;color:#333;font-size:12px; line-height: 14px;font-weight:400;=
        font-family:Arial, Helvetica, sans-serif;margin:0;padding:0;">&#1030;&#1085=
        ;&#1090;&#1077;&#1088;&#1085;&#1077;&#1090;-&#1084;&#1072;&#1075;&#1072;&#1=
        079;&#1080;&#1085; &#171;&#1056;&#1086;&#1079;&#1077;&#1090;&#1082;&#1072;&=
        #8482;&#187;</span></th>=20
        <!--end contact shop-->
        
        
        <th class=3D"small-12 columns small-text-center" style=3D"Margin:0 auto;mar=
        gin:0 auto;padding:0;width:309px;vertical-align: middle;text-align: center;=
        "> <span class=3D"subscribes" style=3D"Margin:0;color:#221F1F;font-size:12p=
        x; line-height: 14px;font-weight:400;margin:0;padding:0;"> <a href=3D"https=
        ://rozetka.com.ua/ua/cabinet/oauth/subscribes/?skey=3DHQQ1CeKZH9jzi42cVPaHa=
        gK/7rM%3D.65177467&amp;iitt=3DVuU9RM4lhMPshF6d4IYj4Dnd4XTT&amp;utm_source=
        =3Ddm&amp;utm_campaign=3Dpersonal_promo&amp;utm_medium=3Demail&amp;xnpe_cmp=
        =3D.eJwTUkgLL7vccvdTt8P52Amyollvpa_simBccmiT5auitAaB0xyKZxlvWDj8uuGolaqvn5S=
        fUqlfkpiUk6pfUqRfkqKfnJpXklqEIgRjRxvFInNRpEzQpDJAiosLEvP0EwFa4TjY.uTCLptQ_R=
        otti-lWLI-2XW0UibU" target=3D"_blank" style=3D"Margin:0;color:#3E77AA;margi=
        n:0;padding:0;text-decoration:none;font-family:Arial, Helvetica, sans-serif=
        ;">&#1042;&#1110;&#1076;&#1087;&#1080;&#1089;&#1072;&#1090;&#1080;&#1089;&#=
        1100; &#1074;&#1110;&#1076; &#1088;&#1086;&#1079;&#1089;&#1080;&#1083;&#108=
        2;&#1080;</a>=20
        </span>=20
        </th>
        
        </tr></table></td>
        </tr><!-- contact end--></table></td>
        </tr></table></td>
        </tr><!-- footer--><!-- text--><tr><td height=3D"8" style=3D"line-height:8p=
        x; height:8px; padding: 0;">&#160;</td></tr><tr><td style=3D"Margin:0;margi=
        n:0;padding:0 16px;vertical-align:middle;"> <span style=3D"color:#999;displ=
        ay:block;font-size:11px;text-align:center;width:100%;font-family:Arial, Hel=
        vetica, sans-serif;font-weight: 400;">&#1051;&#1080;&#1089;&#1090; &#1084;&=
        #1110;&#1089;&#1090;&#1080;&#1090;&#1100; &#1076;&#1072;&#1085;&#1110; &#10=
        76;&#1083;&#1103; &#1076;&#1086;&#1089;&#1090;&#1091;&#1087;&#1091; &#1074;=
         &#1086;&#1089;&#1086;&#1073;&#1080;&#1089;&#1090;&#1080;&#1081; &#1082;&#1=
        072;&#1073;&#1110;&#1085;&#1077;&#1090;, &#1085;&#1077; &#1087;&#1077;&#108=
        8;&#1077;&#1076;&#1072;&#1074;&#1072;&#1081;&#1090;&#1077; &#1081;&#1086;&#=
        1075;&#1086; &#1090;&#1088;&#1077;&#1090;&#1110;&#1084; &#1086;&#1089;&#108=
        6;&#1073;&#1072;&#1084;.</span></td></tr><tr><td style=3D"Margin:0;margin:0=
        ;padding:0 16px;vertical-align:middle;"> <span style=3D"color:#999;display:=
        block;font-size:11px;text-align:center;width:100%;font-family:Arial, Helvet=
        ica, sans-serif;font-weight: 400;">&#1044;&#1086;&#1076;&#1072;&#1081;&#109=
        0;&#1077; &#1085;&#1072;&#1096;&#1091; &#1072;&#1076;&#1088;&#1077;&#1089;&=
        #1091; bestdeal@rozetka.com.ua &#1074; &#1074;&#1072;&#1096; &#1089;&#1087;=
        &#1080;&#1089;&#1086;&#1082; &#1082;&#1086;&#1085;&#1090;&#1072;&#1082;&#10=
        90;&#1110;&#1074;, &#1097;&#1086;&#1073; &#1085;&#1077; &#1087;&#1088;&#108=
        6;&#1087;&#1091;&#1089;&#1090;&#1080;&#1090;&#1080; &#1078;&#1086;&#1076;&#=
        1085;&#1086;&#1111; &#1079;&#1085;&#1080;&#1078;&#1082;&#1080;.</span></td>=
        </tr><tr><td height=3D"8" style=3D"line-height:8px; height:8px; padding: 0;=
        ">&#160;</td></tr><!-- text--></table></td>
        </tr></table></center>
        </td>
        </tr></table><!-- prevent Gmail on iOS font size manipulation --><div style=
        =3D"display:none;white-space:nowrap;font:15px courier;line-height:0">&#160;=
         &#160; &#160; &#160; &#160; &#160; &#160; &#160; &#160; &#160; &#160; &#16=
        0; &#160; &#160; &#160; &#160; &#160; &#160; &#160; &#160; &#160; &#160; &#=
        160; &#160; &#160; &#160; &#160; &#160; &#160; &#160;</div>
        <center><table><tr><td><img src=3D"" width=3D"1" height=3D"1" alt=3D"" titl=
        e=3D"" border=3D"0"></td></tr></table></center></body></html>
        """

        #template = f"""
        #                <html>
        #                    <head>
        #                    </head>
        #                    <body>
        #                        <div style = "display: flex; align-items: center; justify-content: center; flex-direction: column">
        #                            <h3>Account Verification</h3>
        #                            <br>
        #                            <p>Dear Customer, Please open the link:</p>
        #                            <a stle="margin-top: 1rem; padding: 1rem; border-radius: 0.5rem; font-size: 1rem; text-decoration: none; background: #275d8; color: white;" href="{temp_url}{link_to}">{msg_text}</a>
        #                            <p>Please kindly ignore this email if you did not register for our service. Thanks</p>
        #                        </div>
        #                    </body>
        #                </html>
        #            """
    else:
        temp_url = verify_url
        msg_text = "In Order To Change Your Password"

        template = f"""
                                <!DOCTYPE html>
                                <html>
                                    <head>
                                    </head>
                                    <body>
                                        <div style = "display: flex; align-items: center; justify-content: center; flex-direction: column">
                                            <h3>Account Verification</h3>
                                            <br>
                                            <p>Dear Customer, Please open the link:</p>
                                            <a stle="margin-top: 1rem; padding: 1rem; border-radius: 0.5rem; font-size: 1rem; text-decoration: none; background: #275d8; color: white;" href="{temp_url}{link_to}">{msg_text}</a>
                                            <p>Please kindly ignore this email if you did not register for our service. Thanks</p>
                                        </div>
                                    </body>
                                </html>
                            """

    subject_text = ""

    if is_verification:
        subject_text = "Postaty; Verify Your Email"
    else:
        subject_text = "Postaty; Change Your Password"

    print("2---------------------------")
    message = MessageSchema(
        subject=subject_text,
        recipients=[email],  # LIST OF recipients
        body=template,
        subtype="html"
    )

    fm = FastMail(conf)
    print("3---------------------------")
    try:
        await fm.send_message(message=message)
    except:
        return 404

    return 200

