# -*- coding: utf-8 -*-
"""Personvernerklaering v2.1 (10. sep 2026): push-varsler som tjenestemeldinger.

Spleiser fire tekstbiter inn i eksisterende seksjoner (3e, 7, 8, 10) paa
alle 23 spraak og bumper pp_updated. Skriver push_2_1.json som inject.py
tar imot. Kjoer fra repo-rota:
    python _internal/tools/i18n/push_2_1.py && \
    python _internal/tools/i18n/inject.py _internal/tools/i18n/push_2_1.json && \
    node _internal/tools/i18n/validate.js
"""
import json, re, subprocess, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[3]
T = json.loads(subprocess.check_output(
    ['node', '-e',
     "const {T}=require('./_internal/tools/i18n/dump.js');"
     "process.stdout.write(JSON.stringify(T));"],
    cwd=ROOT).decode('utf-8'))

# T1: nytt punkt sist i 3e). T2: nytt avsnitt etter trial-avsnittet i 7.
# T3: hale paa Google Firebase-punktet i 8 (foer </li>). T4: ny linje sist i 10.
# T5: pp_updated.
TX = {
 'en': dict(
  t1='If you allow notifications on your device, a push notification token that identifies the device to Firebase Cloud Messaging. It is linked to your account so that we can reach you with service messages, and is deleted when you turn notifications off, uninstall the app or delete your account',
  t2='We may also send service messages as push notifications to your device &ndash; for example security notices, operational notices and notices of changes to the terms or this privacy policy. You control notifications in your device settings. <strong>We do not send marketing as push notifications</strong>, and we never put health information in a notification.',
  t3=', and push notifications (Firebase Cloud Messaging)',
  t4='<strong>Push notification token</strong> &ndash; until you turn notifications off, uninstall the app or delete your account; tokens that no longer work are deleted automatically.',
  t5='<strong>Last updated:</strong> 10 September 2026 &middot; <strong>Version 2.1</strong>'),
 'nb': dict(
  t1='Hvis du tillater varsler på enheten: et push-token som identifiserer enheten overfor Firebase Cloud Messaging. Det knyttes til kontoen din slik at vi kan nå deg med tjenestemeldinger, og slettes når du skrur av varsler, avinstallerer appen eller sletter kontoen',
  t2='Vi kan også sende tjenestemeldinger som push-varsler til enheten din &ndash; for eksempel sikkerhetsvarsler, driftsmeldinger og varsler om endringer i vilkårene eller denne personvernerklæringen. Du styrer varsler i enhetens innstillinger. <strong>Vi sender ikke markedsføring som push-varsler</strong>, og vi legger aldri helseopplysninger i et varsel.',
  t3=' og push-varsler (Firebase Cloud Messaging)',
  t4='<strong>Push-token</strong> &ndash; til du skrur av varsler, avinstallerer appen eller sletter kontoen; tokener som ikke lenger virker, slettes automatisk.',
  t5='<strong>Sist oppdatert:</strong> 10. september 2026 &middot; <strong>Versjon 2.1</strong>'),
 'da': dict(
  t1='Hvis du tillader notifikationer på enheden: et push-token, der identificerer enheden over for Firebase Cloud Messaging. Det knyttes til din konto, så vi kan nå dig med servicemeddelelser, og slettes, når du slår notifikationer fra, afinstallerer appen eller sletter kontoen',
  t2='Vi kan også sende servicemeddelelser som push-notifikationer til din enhed &ndash; for eksempel sikkerhedsadvarsler, driftsmeddelelser og meddelelser om ændringer i vilkårene eller denne privatlivspolitik. Du styrer notifikationer i enhedens indstillinger. <strong>Vi sender ikke markedsføring som push-notifikationer</strong>, og vi lægger aldrig helbredsoplysninger i en notifikation.',
  t3=' og push-notifikationer (Firebase Cloud Messaging)',
  t4='<strong>Push-token</strong> &ndash; indtil du slår notifikationer fra, afinstallerer appen eller sletter kontoen; tokens, der ikke længere virker, slettes automatisk.',
  t5='<strong>Sidst opdateret:</strong> 10. september 2026 &middot; <strong>Version 2.1</strong>'),
 'sv': dict(
  t1='Om du tillåter aviseringar på enheten: en push-token som identifierar enheten för Firebase Cloud Messaging. Den kopplas till ditt konto så att vi kan nå dig med tjänstemeddelanden, och raderas när du stänger av aviseringar, avinstallerar appen eller raderar kontot',
  t2='Vi kan också skicka tjänstemeddelanden som push-aviseringar till din enhet &ndash; till exempel säkerhetsmeddelanden, driftmeddelanden och meddelanden om ändringar i villkoren eller denna integritetspolicy. Du styr aviseringar i enhetens inställningar. <strong>Vi skickar inte marknadsföring som push-aviseringar</strong>, och vi lägger aldrig hälsouppgifter i en avisering.',
  t3=' och push-aviseringar (Firebase Cloud Messaging)',
  t4='<strong>Push-token</strong> &ndash; tills du stänger av aviseringar, avinstallerar appen eller raderar kontot; tokens som inte längre fungerar raderas automatiskt.',
  t5='<strong>Senast uppdaterad:</strong> 10 september 2026 &middot; <strong>Version 2.1</strong>'),
 'fi': dict(
  t1='Jos sallit ilmoitukset laitteellasi: push-tunniste, joka yksilöi laitteen Firebase Cloud Messagingille. Se liitetään tiliisi, jotta voimme tavoittaa sinut palveluviesteillä, ja se poistetaan, kun poistat ilmoitukset käytöstä, poistat sovelluksen tai poistat tilisi',
  t2='Voimme lähettää palveluviestejä myös push-ilmoituksina laitteellesi &ndash; esimerkiksi tietoturvailmoituksia, käyttöilmoituksia ja ilmoituksia ehtojen tai tämän tietosuojaselosteen muutoksista. Hallitset ilmoituksia laitteesi asetuksissa. <strong>Emme lähetä markkinointia push-ilmoituksina</strong>, emmekä koskaan sisällytä terveystietoja ilmoitukseen.',
  t3=' sekä push-ilmoitukset (Firebase Cloud Messaging)',
  t4='<strong>Push-tunniste</strong> &ndash; kunnes poistat ilmoitukset käytöstä, poistat sovelluksen tai poistat tilisi; toimimattomat tunnisteet poistetaan automaattisesti.',
  t5='<strong>Päivitetty viimeksi:</strong> 10. syyskuuta 2026 &middot; <strong>Versio 2.1</strong>'),
 'de': dict(
  t1='Wenn du Benachrichtigungen auf deinem Gerät erlaubst: ein Push-Token, das das Gerät gegenüber Firebase Cloud Messaging identifiziert. Es wird mit deinem Konto verknüpft, damit wir dich mit Servicemitteilungen erreichen können, und gelöscht, wenn du Benachrichtigungen ausschaltest, die App deinstallierst oder dein Konto löschst',
  t2='Servicemitteilungen können wir auch als Push-Benachrichtigungen an dein Gerät senden &ndash; zum Beispiel Sicherheitshinweise, Betriebsmeldungen und Hinweise auf Änderungen der Bedingungen oder dieser Datenschutzerklärung. Benachrichtigungen steuerst du in den Einstellungen deines Geräts. <strong>Wir versenden keine Werbung als Push-Benachrichtigung</strong>, und wir schreiben niemals Gesundheitsinformationen in eine Benachrichtigung.',
  t3=' sowie Push-Benachrichtigungen (Firebase Cloud Messaging)',
  t4='<strong>Push-Token</strong> &ndash; bis du Benachrichtigungen ausschaltest, die App deinstallierst oder dein Konto löschst; nicht mehr funktionierende Tokens werden automatisch gelöscht.',
  t5='<strong>Zuletzt aktualisiert:</strong> 10. September 2026 &middot; <strong>Version 2.1</strong>'),
 'fr': dict(
  t1='Si vous autorisez les notifications sur votre appareil : un jeton de notification push qui identifie l&rsquo;appareil auprès de Firebase Cloud Messaging. Il est lié à votre compte afin que nous puissions vous joindre avec des messages de service, et il est supprimé lorsque vous désactivez les notifications, désinstallez l&rsquo;application ou supprimez votre compte',
  t2='Nous pouvons aussi envoyer des messages de service sous forme de notifications push sur votre appareil &ndash; par exemple des alertes de sécurité, des informations d&rsquo;exploitation et des avis de modification des conditions ou de la présente politique de confidentialité. Vous gérez les notifications dans les réglages de votre appareil. <strong>Nous n&rsquo;envoyons pas de marketing par notification push</strong>, et nous ne mettons jamais d&rsquo;informations de santé dans une notification.',
  t3=', ainsi que les notifications push (Firebase Cloud Messaging)',
  t4='<strong>Jeton de notification push</strong> &ndash; jusqu&rsquo;à ce que vous désactiviez les notifications, désinstalliez l&rsquo;application ou supprimiez votre compte ; les jetons qui ne fonctionnent plus sont supprimés automatiquement.',
  t5='<strong>Dernière mise à jour :</strong> 10 septembre 2026 &middot; <strong>Version 2.1</strong>'),
 'es': dict(
  t1='Si permites las notificaciones en tu dispositivo: un token de notificaciones push que identifica el dispositivo ante Firebase Cloud Messaging. Se vincula a tu cuenta para que podamos enviarte mensajes de servicio, y se elimina cuando desactivas las notificaciones, desinstalas la app o eliminas tu cuenta',
  t2='También podemos enviar mensajes de servicio como notificaciones push a tu dispositivo &ndash; por ejemplo avisos de seguridad, avisos operativos y avisos de cambios en los términos o en esta política de privacidad. Tú controlas las notificaciones en los ajustes de tu dispositivo. <strong>No enviamos marketing por notificaciones push</strong>, y nunca incluimos información de salud en una notificación.',
  t3=' y notificaciones push (Firebase Cloud Messaging)',
  t4='<strong>Token de notificaciones push</strong> &ndash; hasta que desactives las notificaciones, desinstales la app o elimines tu cuenta; los tokens que dejan de funcionar se eliminan automáticamente.',
  t5='<strong>Última actualización:</strong> 10 de septiembre de 2026 &middot; <strong>Versión 2.1</strong>'),
 'it': dict(
  t1='Se consenti le notifiche sul tuo dispositivo: un token di notifica push che identifica il dispositivo presso Firebase Cloud Messaging. È collegato al tuo account affinché possiamo raggiungerti con messaggi di servizio, e viene eliminato quando disattivi le notifiche, disinstalli l&rsquo;app o elimini l&rsquo;account',
  t2='Possiamo inviare messaggi di servizio anche come notifiche push sul tuo dispositivo &ndash; ad esempio avvisi di sicurezza, comunicazioni operative e avvisi di modifica dei termini o della presente informativa sulla privacy. Gestisci le notifiche nelle impostazioni del dispositivo. <strong>Non inviamo marketing tramite notifiche push</strong>, e non inseriamo mai informazioni sulla salute in una notifica.',
  t3=' e notifiche push (Firebase Cloud Messaging)',
  t4='<strong>Token di notifica push</strong> &ndash; finché non disattivi le notifiche, disinstalli l&rsquo;app o elimini l&rsquo;account; i token che non funzionano più vengono eliminati automaticamente.',
  t5='<strong>Ultimo aggiornamento:</strong> 10 settembre 2026 &middot; <strong>Versione 2.1</strong>'),
 'pt': dict(
  t1='Se você permitir notificações no seu dispositivo: um token de notificação push que identifica o dispositivo junto ao Firebase Cloud Messaging. Ele é vinculado à sua conta para que possamos alcançá-lo com mensagens de serviço, e é excluído quando você desativa as notificações, desinstala o app ou exclui sua conta',
  t2='Também podemos enviar mensagens de serviço como notificações push para o seu dispositivo &ndash; por exemplo avisos de segurança, avisos operacionais e avisos de alterações nos termos ou nesta política de privacidade. Você controla as notificações nas configurações do seu dispositivo. <strong>Não enviamos marketing por notificações push</strong>, e nunca colocamos informações de saúde em uma notificação.',
  t3=' e notificações push (Firebase Cloud Messaging)',
  t4='<strong>Token de notificação push</strong> &ndash; até você desativar as notificações, desinstalar o app ou excluir sua conta; tokens que deixam de funcionar são excluídos automaticamente.',
  t5='<strong>Última atualização:</strong> 10 de setembro de 2026 &middot; <strong>Versão 2.1</strong>'),
 'nl': dict(
  t1='Als je meldingen op je apparaat toestaat: een pushmeldingstoken dat het apparaat identificeert bij Firebase Cloud Messaging. Het wordt aan je account gekoppeld zodat we je servicemeldingen kunnen sturen, en wordt verwijderd wanneer je meldingen uitschakelt, de app verwijdert of je account verwijdert',
  t2='We kunnen servicemeldingen ook als pushmeldingen naar je apparaat sturen &ndash; bijvoorbeeld beveiligingsmeldingen, operationele meldingen en meldingen over wijzigingen in de voorwaarden of dit privacybeleid. Je beheert meldingen in de instellingen van je apparaat. <strong>We sturen geen marketing als pushmelding</strong>, en we zetten nooit gezondheidsinformatie in een melding.',
  t3=' en pushmeldingen (Firebase Cloud Messaging)',
  t4='<strong>Pushmeldingstoken</strong> &ndash; totdat je meldingen uitschakelt, de app verwijdert of je account verwijdert; tokens die niet meer werken worden automatisch verwijderd.',
  t5='<strong>Laatst bijgewerkt:</strong> 10 september 2026 &middot; <strong>Versie 2.1</strong>'),
 'pl': dict(
  t1='Jeśli zezwolisz na powiadomienia na swoim urządzeniu: token powiadomień push, który identyfikuje urządzenie w Firebase Cloud Messaging. Jest powiązany z Twoim kontem, abyśmy mogli przekazywać Ci komunikaty serwisowe, i jest usuwany, gdy wyłączysz powiadomienia, odinstalujesz aplikację lub usuniesz konto',
  t2='Komunikaty serwisowe możemy wysyłać także jako powiadomienia push na Twoje urządzenie &ndash; na przykład ostrzeżenia dotyczące bezpieczeństwa, komunikaty operacyjne oraz informacje o zmianach regulaminu lub niniejszej polityki prywatności. Powiadomieniami zarządzasz w ustawieniach urządzenia. <strong>Nie wysyłamy marketingu w formie powiadomień push</strong> i nigdy nie umieszczamy informacji o zdrowiu w powiadomieniu.',
  t3=' oraz powiadomienia push (Firebase Cloud Messaging)',
  t4='<strong>Token powiadomień push</strong> &ndash; do czasu wyłączenia powiadomień, odinstalowania aplikacji lub usunięcia konta; tokeny, które przestały działać, są usuwane automatycznie.',
  t5='<strong>Ostatnia aktualizacja:</strong> 10 września 2026 &middot; <strong>Wersja 2.1</strong>'),
 'ru': dict(
  t1='Если вы разрешили уведомления на устройстве: push-токен, который идентифицирует устройство для Firebase Cloud Messaging. Он привязывается к вашему аккаунту, чтобы мы могли отправлять вам сервисные сообщения, и удаляется, когда вы отключаете уведомления, удаляете приложение или аккаунт',
  t2='Сервисные сообщения мы можем отправлять и в виде push-уведомлений на ваше устройство &ndash; например, уведомления о безопасности, о работе сервиса и об изменениях условий или настоящей политики конфиденциальности. Уведомлениями вы управляете в настройках устройства. <strong>Мы не рассылаем маркетинг через push-уведомления</strong> и никогда не включаем в уведомление сведения о здоровье.',
  t3=', а также push-уведомления (Firebase Cloud Messaging)',
  t4='<strong>Push-токен</strong> &ndash; пока вы не отключите уведомления, не удалите приложение или аккаунт; недействительные токены удаляются автоматически.',
  t5='<strong>Последнее обновление:</strong> 10 сентября 2026 г. &middot; <strong>Версия 2.1</strong>'),
 'tr': dict(
  t1='Cihazınızda bildirimlere izin verirseniz: cihazı Firebase Cloud Messaging&rsquo;e tanıtan bir push bildirimi belirteci. Size hizmet mesajları ulaştırabilmemiz için hesabınıza bağlanır; bildirimleri kapattığınızda, uygulamayı kaldırdığınızda veya hesabınızı sildiğinizde silinir',
  t2='Hizmet mesajlarını cihazınıza push bildirimi olarak da gönderebiliriz &ndash; örneğin güvenlik uyarıları, işletim duyuruları ve koşullarda ya da bu gizlilik politikasında yapılan değişikliklere ilişkin bildirimler. Bildirimleri cihazınızın ayarlarından yönetirsiniz. <strong>Push bildirimi olarak pazarlama göndermeyiz</strong> ve bir bildirime asla sağlık bilgisi koymayız.',
  t3=' ve push bildirimleri (Firebase Cloud Messaging)',
  t4='<strong>Push bildirimi belirteci</strong> &ndash; bildirimleri kapatana, uygulamayı kaldırana veya hesabınızı silene kadar; artık çalışmayan belirteçler otomatik olarak silinir.',
  t5='<strong>Son güncelleme:</strong> 10 Eylül 2026 &middot; <strong>Sürüm 2.1</strong>'),
 'ja': dict(
  t1='端末で通知を許可している場合：Firebase Cloud Messaging に対して端末を識別するプッシュ通知トークン。サービスに関するお知らせをお届けするためアカウントに紐づけられ、通知をオフにしたとき、アプリをアンインストールしたとき、またはアカウントを削除したときに削除されます',
  t2='サービスに関するお知らせは、端末へのプッシュ通知としてお送りすることもあります &ndash; たとえばセキュリティ上の通知、運用上の通知、利用規約や本プライバシーポリシーの変更に関する通知です。通知は端末の設定で管理できます。<strong>プッシュ通知でマーケティングを送ることはありません</strong>。また、通知に健康に関する情報を含めることは決してありません。',
  t3='、およびプッシュ通知（Firebase Cloud Messaging）',
  t4='<strong>プッシュ通知トークン</strong> &ndash; 通知をオフにする、アプリをアンインストールする、またはアカウントを削除するまで。無効になったトークンは自動的に削除されます。',
  t5='<strong>最終更新日：</strong>2026年9月10日 &middot; <strong>バージョン 2.1</strong>'),
 'ko': dict(
  t1='기기에서 알림을 허용한 경우: Firebase Cloud Messaging에 기기를 식별해 주는 푸시 알림 토큰. 서비스 메시지를 전달할 수 있도록 계정에 연결되며, 알림을 끄거나 앱을 삭제하거나 계정을 삭제하면 삭제됩니다',
  t2='서비스 메시지는 기기로 보내는 푸시 알림 형태로도 전송할 수 있습니다 &ndash; 예를 들어 보안 안내, 운영 안내, 약관 또는 본 개인정보 처리방침의 변경 안내입니다. 알림은 기기 설정에서 관리할 수 있습니다. <strong>푸시 알림으로 마케팅을 보내지 않으며</strong>, 알림에 건강 정보를 넣는 일은 결코 없습니다.',
  t3=', 푸시 알림(Firebase Cloud Messaging)',
  t4='<strong>푸시 알림 토큰</strong> &ndash; 알림을 끄거나 앱을 삭제하거나 계정을 삭제할 때까지 보관되며, 더 이상 작동하지 않는 토큰은 자동으로 삭제됩니다.',
  t5='<strong>최종 업데이트:</strong> 2026년 9월 10일 &middot; <strong>버전 2.1</strong>'),
 'zh-Hans': dict(
  t1='如果您允许设备接收通知：一个向 Firebase Cloud Messaging 标识该设备的推送通知令牌。它与您的账户关联，以便我们向您发送服务消息；当您关闭通知、卸载应用或删除账户时，它会被删除',
  t2='我们也可能以推送通知的形式向您的设备发送服务消息 &ndash; 例如安全提醒、运营通知，以及条款或本隐私政策变更的通知。您可以在设备设置中管理通知。<strong>我们不会通过推送通知发送营销内容</strong>，也绝不会在通知中包含健康信息。',
  t3='以及推送通知（Firebase Cloud Messaging）',
  t4='<strong>推送通知令牌</strong> &ndash; 保留至您关闭通知、卸载应用或删除账户为止；失效的令牌会被自动删除。',
  t5='<strong>最后更新：</strong>2026 年 9 月 10 日 &middot; <strong>版本 2.1</strong>'),
 'zh-Hant': dict(
  t1='如果您允許裝置接收通知：一個向 Firebase Cloud Messaging 識別該裝置的推播通知權杖。它與您的帳戶連結，以便我們向您傳送服務訊息；當您關閉通知、解除安裝應用程式或刪除帳戶時，它會被刪除',
  t2='我們也可能以推播通知的形式向您的裝置傳送服務訊息 &ndash; 例如安全提醒、營運通知，以及條款或本隱私權政策變更的通知。您可以在裝置設定中管理通知。<strong>我們不會透過推播通知傳送行銷內容</strong>，也絕不會在通知中包含健康資訊。',
  t3='以及推播通知（Firebase Cloud Messaging）',
  t4='<strong>推播通知權杖</strong> &ndash; 保留至您關閉通知、解除安裝應用程式或刪除帳戶為止；失效的權杖會被自動刪除。',
  t5='<strong>最後更新：</strong>2026 年 9 月 10 日 &middot; <strong>版本 2.1</strong>'),
 'hi': dict(
  t1='यदि आप अपने डिवाइस पर सूचनाओं की अनुमति देते हैं: एक पुश नोटिफ़िकेशन टोकन, जो Firebase Cloud Messaging के लिए डिवाइस की पहचान करता है। यह आपके खाते से जुड़ा रहता है ताकि हम आपको सेवा संदेश भेज सकें, और जब आप सूचनाएँ बंद करते हैं, ऐप हटाते हैं या खाता हटाते हैं तो इसे हटा दिया जाता है',
  t2='हम सेवा संदेश आपके डिवाइस पर पुश नोटिफ़िकेशन के रूप में भी भेज सकते हैं &ndash; जैसे सुरक्षा सूचनाएँ, परिचालन सूचनाएँ और शर्तों या इस गोपनीयता नीति में बदलाव की सूचनाएँ। सूचनाओं को आप अपने डिवाइस की सेटिंग में नियंत्रित करते हैं। <strong>हम पुश नोटिफ़िकेशन के रूप में मार्केटिंग नहीं भेजते</strong>, और किसी सूचना में स्वास्थ्य संबंधी जानकारी कभी नहीं डालते।',
  t3=' और पुश नोटिफ़िकेशन (Firebase Cloud Messaging)',
  t4='<strong>पुश नोटिफ़िकेशन टोकन</strong> &ndash; जब तक आप सूचनाएँ बंद नहीं करते, ऐप नहीं हटाते या खाता नहीं हटाते; जो टोकन काम करना बंद कर देते हैं, वे अपने आप हटा दिए जाते हैं।',
  t5='<strong>अंतिम अपडेट:</strong> 10 सितंबर 2026 &middot; <strong>संस्करण 2.1</strong>'),
 'id': dict(
  t1='Jika Anda mengizinkan notifikasi di perangkat: token notifikasi push yang mengidentifikasi perangkat ke Firebase Cloud Messaging. Token ini ditautkan ke akun Anda agar kami dapat mengirimkan pesan layanan, dan dihapus saat Anda mematikan notifikasi, mencopot pemasangan aplikasi, atau menghapus akun',
  t2='Kami juga dapat mengirim pesan layanan sebagai notifikasi push ke perangkat Anda &ndash; misalnya pemberitahuan keamanan, pemberitahuan operasional, dan pemberitahuan perubahan ketentuan atau kebijakan privasi ini. Anda mengatur notifikasi di pengaturan perangkat. <strong>Kami tidak mengirim pemasaran melalui notifikasi push</strong>, dan tidak pernah mencantumkan informasi kesehatan dalam notifikasi.',
  t3=', serta notifikasi push (Firebase Cloud Messaging)',
  t4='<strong>Token notifikasi push</strong> &ndash; hingga Anda mematikan notifikasi, mencopot pemasangan aplikasi, atau menghapus akun; token yang tidak lagi berfungsi dihapus secara otomatis.',
  t5='<strong>Terakhir diperbarui:</strong> 10 September 2026 &middot; <strong>Versi 2.1</strong>'),
 'lt': dict(
  t1='Jei leidžiate pranešimus savo įrenginyje: tiesioginių pranešimų prieigos raktas, kuris identifikuoja įrenginį „Firebase Cloud Messaging“ sistemoje. Jis susiejamas su jūsų paskyra, kad galėtume jus pasiekti paslaugų pranešimais, ir ištrinamas, kai išjungiate pranešimus, pašalinate programėlę arba ištrinate paskyrą',
  t2='Paslaugų pranešimus galime siųsti ir kaip tiesioginius pranešimus į jūsų įrenginį &ndash; pavyzdžiui, saugumo įspėjimus, veiklos pranešimus ir pranešimus apie sąlygų ar šios privatumo politikos pakeitimus. Pranešimus valdote įrenginio nustatymuose. <strong>Rinkodaros tiesioginiais pranešimais nesiunčiame</strong>, o sveikatos informacijos į pranešimą niekada neįtraukiame.',
  t3=' ir tiesioginiai pranešimai („Firebase Cloud Messaging“)',
  t4='<strong>Tiesioginių pranešimų prieigos raktas</strong> &ndash; kol išjungsite pranešimus, pašalinsite programėlę arba ištrinsite paskyrą; nebeveikiantys raktai ištrinami automatiškai.',
  t5='<strong>Paskutinį kartą atnaujinta:</strong> 2026 m. rugsėjo 10 d. &middot; <strong>Versija 2.1</strong>'),
 'th': dict(
  t1='หากคุณอนุญาตการแจ้งเตือนบนอุปกรณ์: โทเค็นการแจ้งเตือนแบบพุชที่ระบุตัวอุปกรณ์ต่อ Firebase Cloud Messaging โทเค็นนี้เชื่อมโยงกับบัญชีของคุณเพื่อให้เราส่งข้อความเกี่ยวกับบริการถึงคุณได้ และจะถูกลบเมื่อคุณปิดการแจ้งเตือน ถอนการติดตั้งแอป หรือลบบัญชี',
  t2='เราอาจส่งข้อความเกี่ยวกับบริการเป็นการแจ้งเตือนแบบพุชไปยังอุปกรณ์ของคุณด้วย &ndash; เช่น การแจ้งเตือนด้านความปลอดภัย ประกาศด้านการดำเนินงาน และการแจ้งการเปลี่ยนแปลงข้อกำหนดหรือนโยบายความเป็นส่วนตัวนี้ คุณควบคุมการแจ้งเตือนได้ในการตั้งค่าอุปกรณ์ <strong>เราไม่ส่งการตลาดผ่านการแจ้งเตือนแบบพุช</strong> และไม่ใส่ข้อมูลสุขภาพในการแจ้งเตือนโดยเด็ดขาด',
  t3=' และการแจ้งเตือนแบบพุช (Firebase Cloud Messaging)',
  t4='<strong>โทเค็นการแจ้งเตือนแบบพุช</strong> &ndash; จนกว่าคุณจะปิดการแจ้งเตือน ถอนการติดตั้งแอป หรือลบบัญชี โทเค็นที่ใช้งานไม่ได้แล้วจะถูกลบโดยอัตโนมัติ',
  t5='<strong>อัปเดตล่าสุด:</strong> 10 กันยายน 2026 &middot; <strong>เวอร์ชัน 2.1</strong>'),
 'ar': dict(
  t1='إذا سمحت بالإشعارات على جهازك: رمز إشعارات فورية يعرّف الجهاز لدى Firebase Cloud Messaging. يُربط بحسابك حتى نتمكن من إيصال رسائل الخدمة إليك، ويُحذف عند إيقاف الإشعارات أو إلغاء تثبيت التطبيق أو حذف حسابك',
  t2='قد نرسل رسائل الخدمة أيضاً كإشعارات فورية إلى جهازك &ndash; مثل تنبيهات الأمان، وإشعارات التشغيل، وإشعارات التغييرات في الشروط أو في سياسة الخصوصية هذه. تتحكم في الإشعارات من إعدادات جهازك. <strong>لا نرسل تسويقاً عبر الإشعارات الفورية</strong>، ولا نضع أبداً معلومات صحية في أي إشعار.',
  t3=' والإشعارات الفورية (Firebase Cloud Messaging)',
  t4='<strong>رمز الإشعارات الفورية</strong> &ndash; حتى تُوقف الإشعارات أو تُلغي تثبيت التطبيق أو تحذف حسابك؛ وتُحذف الرموز التي لم تعد تعمل تلقائياً.',
  t5='<strong>آخر تحديث:</strong> 10 سبتمبر 2026 &middot; <strong>الإصدار 2.1</strong>'),
}
assert set(TX) == set(T), set(T) ^ set(TX)


def nth(s, sub, n):
    i = -1
    for _ in range(n):
        i = s.index(sub, i + 1)
    return i


ut = {}
for lang, tx in TX.items():
    t = T[lang]
    s3, s7, s8, s10 = t['pp_s3p'], t['pp_s7p'], t['pp_s8p'], t['pp_s10p']
    assert 'Firebase Cloud Messaging' not in s3 + s7 + s8 + s10, lang  # idempotens
    # 3e): nytt punkt sist i femte liste.
    i = nth(s3, '</ul>', 5)
    s3 = s3[:i] + '<li>' + tx['t1'] + '</li>' + s3[i:]
    # 7: nytt avsnitt etter det andre avsnittet (trial-avsnittet beholdes).
    i = nth(s7, '</p>', 2) + len('</p>')
    s7 = s7[:i] + '<p>' + tx['t2'] + '</p>' + s7[i:]
    # 8: hale paa foerste punkt (Google Firebase).
    i = s8.index('</li>')
    s8 = s8[:i] + tx['t3'] + s8[i:]
    # 10: ny linje sist.
    i = s10.rindex('</ul>')
    s10 = s10[:i] + '<li>' + tx['t4'] + '</li>' + s10[i:]
    ut[lang] = dict(pp_s3p=s3, pp_s7p=s7, pp_s8p=s8, pp_s10p=s10,
                    pp_updated=tx['t5'])

(ROOT / '_internal/tools/i18n/push_2_1.json').write_text(
    json.dumps(ut, ensure_ascii=False, indent=1), encoding='utf-8')
print('push_2_1.json:', len(ut), 'spraak x 5 noekler')
