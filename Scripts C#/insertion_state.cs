using System;
using System.Collections;
using System.Collections.Generic;
using System.Data;
using Unity.VisualScripting;
using UnityEngine;
using static UnityEngine.GraphicsBuffer;

public class insertion_state : FactoryBaseState
{
    public override void EnterState(StateManager factory)
    {
        // le produit est transporter jusqu'au position2
        //Debug.Log("state 2 entered at timestamp : " + Time.time);
        gameObject.GetComponent<Animator>().enabled = true;
        gameObject.GetComponent<Animator>().SetBool("accept", true);
        gameObject.GetComponent<Animator>().SetTrigger("first_rot");
        StartCoroutine(TillAnimCoroutine2());
    }
    public override void UpdateState(StateManager factory){}

    public override void OnCollisionEnter_(StateManager factory, Collider collision)
    {
        // L'orsque le capteur detecte l'arrivé du produit l'arm'01 commence son travail
        if (collision.gameObject.name == "arm-01-collider")
        {
            GameObject.FindWithTag("Armc-01").GetComponent<Animation>().Play();
        }
        // on declanche une courotine de 5s jusqu'a ce que l'arm'01 termine son travail
        StartCoroutine(TillAnimCoroutine(factory));
    }
    IEnumerator TillAnimCoroutine(StateManager factory)
    {
        //Debug.Log("Started Coroutine at timestamp : " + Time.time);
        yield return new WaitForSeconds(5f);
        transform.GetChild(2).gameObject.SetActive(true);
        // on declanche l'etat suivant
        factory.SwitchState(factory.inspectionState);
    }
    IEnumerator TillAnimCoroutine2()
    {
        yield return new WaitForSeconds(8f);
        gameObject.GetComponent<Animator>().SetBool("accept", false);
        gameObject.GetComponent<Animator>().enabled = false;
    }
}
