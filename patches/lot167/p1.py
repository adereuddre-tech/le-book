# Lot 167 : dépêches émises par une institution (banque centrale, Trésor, bourse, OPEP, météo…) — une icône adaptée à la place
# d'un visage générique ; les personnes gardent leur portrait.
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep("function evHead(who,kind){const P=personOf(who||'');",r'''const EVICO=[[/banque centrale|BCE|Fed|Réserve fédérale|gouverneur|banque du Japon|BoE|banque d'Angleterre|BNS|monétaire/i,'🏦'],[/Trésor|ministère|gouvernement|Congrès|parlement|vote|élection|présiden|Bruxelles|Commission|sommet/i,'🏛️'],
 [/OPEP|pétrol|baril|raffiner|gaz|énergie|oléoduc/i,'🛢️'],[/blé|récolte|café|cacao|agricole|Chicago|sécheresse|mousson/i,'🌾'],[/météo|ouragan|typhon|séisme|climat|inondation|tempête/i,'🌪️'],
 [/guerre|armée|missile|militaire|frontière|sanction|embargo|attentat|coup d'État/i,'⚔️'],[/bourse|indice|cotation|marché|séance/i,'📈'],[/crypto|bitcoin|stablecoin|blockchain/i,'🪙'],
 [/régulat|autorité|tribunal|juge|enquête|amende|SEC/i,'⚖️'],[/statisti|emploi|PIB|inflation|chômage|enquête PMI|données|INSEE|BLS/i,'📊'],[/agence de notation|notation|Moody|S&P Global|Fitch/i,'🏷️'],
 [/banque|faillite|crédit|dette|obligat|spread/i,'💳'],[/presse|journal|dépêche|agence|Bloomberg|Reuters/i,'📰']];
function evIco(who,t){const x=(who||'')+' '+(t||'');for(const [rx,ic] of EVICO)if(rx.test(x))return ic;return '📰'}
function evHead(who,kind){const P=personOf(who||'');
 if(kind==='news'&&!P&&!personGen(who||''))return `<div class="evhead"><span class="evico">${evIco(who,'')}</span><div class="who">${(who||'').toUpperCase()}</div></div>`;''')
rep(".evhead .pic{",".evhead .evico{font-size:34px;width:46px;height:46px;display:inline-flex;align-items:center;justify-content:center;border-radius:50%;border:2px solid var(--gold);background:var(--panel2);margin-right:8px}\n.evhead .pic{")
open('index.html','w',encoding='utf-8').write(s);print('lot167 ok')
