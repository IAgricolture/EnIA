In questa cartella è contenuta la documentazione generata automaticamente da sphinx. Per visualizzarla, si parte dal file index.html in build.
Per aggiunte o modifiche al progetto, è sufficiente eseguire il comando make html.
Per rigenerare lo schema di documentazione da capo (necessarie modifiche manuali):
    cd documentation
    sphinx-apidoc -f -o ../documentation/source ../src/logic (ATTENZIONE: Sovrascrive documentazione precedentemente esistente)
    make html   //Rigenera la pagina.