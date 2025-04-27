using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class packaging_state : FactoryBaseState
{
    public override void EnterState(StateManager factory)
    {
        //Debug.Log("state 4 entered at timestamp : " + Time.time);
        // le produit est transporter jusqu'au position suivante
        gameObject.GetComponent<Animation>().Play("Second Rotation");
        StartCoroutine(TillAnimCoroutine3());
    }
    public override void UpdateState(StateManager factory){}

    public override void OnCollisionEnter_(StateManager factory, Collider collision)
    {
        // L'orsque le capteur detecte l'arrivé du produit l'arm02 commence son travail
        if (collision.gameObject.name == "arm-02-collider")
        {
            GameObject.FindWithTag("Armc-02").GetComponent<Animation>().Play();
        }
        // on declanche une courotine de 5s jusqu'a ce que l'arm02 termine son travail
        StartCoroutine(TillAnimCoroutine(factory));
    }
    IEnumerator TillAnimCoroutine(StateManager factory)
    {
        //Debug.Log("Started Coroutine at timestamp : " + Time.time);
        yield return new WaitForSeconds(5f);
        transform.GetChild(3).GetComponent<MeshRenderer>().enabled = true;
        // on declanche l'etat FINALE
        factory.SwitchState(factory.finalState);
        //Debug.Log("Finished Coroutine at timestamp : " + Time.time);
    }
    IEnumerator TillAnimCoroutine3()
    {
        yield return new WaitForSeconds(8f);
    }
}
