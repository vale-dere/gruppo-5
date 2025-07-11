# gruppo-5 - AnonimaData

# AnonimaData

**AnonimaData** è una moderna web application progettata per facilitare l’anonimizzazione di dataset tabulari secondo i principali modelli di privacy-preserving data publishing. Il progetto è stato realizzato da **Valentina de Respinis** e **Danila Meleleo** per l'esame di Scalable and Reliable Systems M a.a 2024/2025.

+++ [Relazione (PDF)](./AnonimaData_report.pdf)

---

## Abstract

In un’epoca dominata dal big data, condividere dataset è pratica comune in settori come sanità, finanza, marketing e pubblica amministrazione. Tuttavia, la protezione della privacy resta una sfida critica. Anche dopo aver rimosso identificatori diretti (come nome o email), individui possono essere re-identificati tramite attributi apparentemente innocui — i cosiddetti **quasi-identificatori** (es. età, CAP, genere).

Modelli come **k-anonymity**, **ℓ-diversity**, **t-closeness** e **differential privacy** sono stati sviluppati per rispondere a queste esigenze. Tuttavia, la loro applicazione pratica è spesso ostacolata da strumenti poco scalabili o complessi da usare.

**AnonimaData** affronta questo problema offrendo una soluzione scalabile, cloud-based e accessibile via interfaccia web. L’utente può caricare dataset, selezionare l’algoritmo di anonimizzazione, configurarne i parametri e ottenere in output un file anonimizzato e pronto all’uso.

---

## Funzionalità principali

- Upload di file CSV o JSON
- Selezione algoritmi: `k-anonymity`, `ℓ-diversity`, `t-closeness`, `differential privacy`
- Configurazione dinamica dei parametri (es. valore di `k`)
- Preview in tempo reale del dataset anonimizzato
- Download del dataset finale (cloud o locale)
- Autenticazione sicura via Firebase (Google OAuth 2.0)
- Backend asincrono e documentato (FastAPI)
- Deploy completo su Google Cloud Platform via Terraform

---

## Architettura

- **Frontend**: Web app moderna (React), servita via Cloud Run
- **Backend**: FastAPI, gestione asincrona dei task, logging centralizzato
- **Storage**: Google Cloud Storage + Firestore
- **Auth**: Firebase Authentication
- **IaC**: Terraform per provisioning e deploy automatizzato

---

## Relazione

La documentazione completa del progetto, con architettura, scelte di design, limitazioni e possibili estensioni future è disponibile nel PDF allegato.

+++ [Relazione (PDF)](./AnonimaData_report.pdf)


---

## Video demo

Un video demo dimostrativo è presente al link allegato e nella repository

+++ [Video demo](./presentazione/VideoAnonimaData.mp4)

---

## Autori

- **Valentina de Respinis**
- **Danila Meleleo**



