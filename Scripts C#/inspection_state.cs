using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class inspection_state : FactoryBaseState
{
    public float speed=1;

    public override void EnterState(StateManager factory)
    {
        //Debug.Log("state 3 entered at timestamp: " + Time.time);
    }
    public override void UpdateState(StateManager factory)
    {
        // le produit est transporter jusqu'au position3
        gameObject.transform.position = Vector3.MoveTowards(gameObject.transform.position, GameObject.FindWithTag("pos3").transform.position, speed * Time.deltaTime);
    }
    public override void OnCollisionEnter_(StateManager factory, Collider collision)
    {
        // L'orsque le capteur detecte l'arrivé du produit la Machine02 commence son travail
        if (collision.gameObject.name == "m-02-collider")
        {
            GameObject.FindWithTag("Machine-02").GetComponent<Animation>().Play();
        }
        // on declanche une courotine de 2s jusqu'a ce que la machine02 termine son travail
        StartCoroutine(TillAnimCoroutine(factory));


    }
    IEnumerator TillAnimCoroutine(StateManager factory)
    {
        //Debug.Log("Started Coroutine at timestamp : " + Time.time);
        yield return new WaitForSeconds(2f);
        // on declanche l'etat suivant
        factory.SwitchState(factory.packagingState);
        //Debug.Log("Finished Coroutine at timestamp : " + Time.time);
    }
}
