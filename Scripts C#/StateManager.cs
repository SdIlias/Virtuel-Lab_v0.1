using System;
using System.Collections;
using System.Collections.Generic;
using Unity.VisualScripting;
using UnityEngine;


public class StateManager : MonoBehaviour
{
    FactoryBaseState currentState;
    // Declarations de toutes les etats
    public init_state initState = new init_state();
    public insertion_state insertionState = new insertion_state();
    public inspection_state inspectionState = new inspection_state();
    public packaging_state packagingState = new packaging_state();
    public final_state finalState = new final_state();

    // cette methode est une methode par defauts de UNITY se lance une fois l'application est ouverte
    void Start()
    {
        //Instantiations des etats
        initState = gameObject.GetComponent<init_state>();
        insertionState = gameObject.GetComponent<insertion_state>();
        inspectionState = gameObject.GetComponent<inspection_state>();
        packagingState = gameObject.GetComponent<packaging_state>();
        finalState = gameObject.GetComponent<final_state>();
        //Declare l'etat initiale
        currentState = initState;
        currentState.EnterState(this);
    }
    // OnTriggerEnter est une methode de unity declanché une fois un object entre dans une zone
    public void OnTriggerEnter(Collider collision)
    {
        //on lie OnTriggerEnter a notre methode OnCollisionEnter_
        currentState.OnCollisionEnter_(this, collision);
    }
    // cette methode de UNITY se lance chaque frame
    void Update()
    {
        //on lie Update a notre methode UpdateState
        currentState.UpdateState(this);     
    }
    // C'est la fonction qui gere les transitions entre les etats
    public void SwitchState(FactoryBaseState state)
    {
        currentState = state;
        state.EnterState(this);
    }
}
